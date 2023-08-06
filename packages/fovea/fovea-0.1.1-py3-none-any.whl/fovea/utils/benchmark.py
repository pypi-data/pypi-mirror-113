import torch
import time
import random
import numpy as np
import itertools
from .timer import Timer
from collections import OrderedDict
from tabulate import tabulate


__all__ = ["TestCase", "BenchmarkRunner"]


class TestCase:
    def __init__(
        self,
        name,
        tags=None,
        is_cuda=False,
        is_warmup=False,
        torch_enable_grad=False,
        n_best=10,
        n_total=100,
        mean_time_unit="auto",
        std_time_unit="auto",
    ):
        """
        Args:
            is_warmup: True to run the test but ignore the output.
                Useful for CUDA tests that require warming up GPU.
        """
        self.name = name
        if tags is None:
            tags = ()
        elif isinstance(tags, str):
            tags = (tags,)
        else:
            assert isinstance(tags, (list, tuple))
            tags = tuple(tags)
        self.tags = tags
        self._is_cuda = is_cuda
        self._is_warmup = is_warmup
        if torch_enable_grad:
            self._grad_context = torch.enable_grad()
        else:
            self._grad_context = torch.no_grad()
        if n_best is None:
            n_best = n_total
        assert n_best <= n_total
        self._n_best = n_best
        self._n_total = n_total
        self._mean_time_unit = mean_time_unit
        self._std_time_unit = std_time_unit
        self._avg_best = self._avg_total = self._min = self._max = None

    def setup(self):
        pass

    def body(self):
        raise NotImplementedError

    def teardown(self):
        pass

    def _run(self, verbose):
        repeats = []
        with self._grad_context:
            self.setup()
        for _ in range(self._n_total):
            start = time.time()
            with self._grad_context:
                self.body()
            if self._is_cuda:
                torch.cuda.synchronize()
            repeats.append(time.time() - start)
            torch.cuda.empty_cache()
        self.teardown()
        repeats = np.sort(np.array(repeats))
        self._avg_best = "{} \u00B1 {}".format(
            Timer.pformat(repeats[: self._n_best].mean(), unit=self._mean_time_unit),
            Timer.pformat(repeats[: self._n_best].std(), unit=self._std_time_unit),
        )
        self._avg_total = "{} \u00B1 {}".format(
            Timer.pformat(repeats.mean(), unit=self._mean_time_unit),
            Timer.pformat(repeats.std(), unit=self._std_time_unit),
        )
        self._min = Timer.pformat(repeats.min(), unit=self._mean_time_unit)
        self._max = Timer.pformat(repeats.max(), unit=self._mean_time_unit)
        if verbose:
            print(
                "avg_best={}, avg_total={}, min={}, max={}\t{}".format(
                    self._avg_best, self._avg_total, self._min, self._max, self.name
                )
            )


class BenchmarkRunner:
    def __init__(
        self,
        test_cases,
        randomize=True,
        group_tag_cartesian=None,
        group_tag_flat=None,
        tag_headers=None,
        tag_display_mode="column",
        verbose=True,
    ):
        """
        Args:
            group_tag_cartesian: provide a list of list of tags, and generates
                a cartesian product list of tag groups
                e.g. [['forward', 'backward'], ['fp16', 'fp32']]
                generates [['forward', 'fp16'], ['forward', 'fp32'],
                        .. ['backward', 'fp16'], ['backward', 'fp32']]
                --OR--
                set group_tag_cartesian='auto' to automatically generate
                    cartesian product from your tags
            group_tag_flat: provide a list of tag lists as flat tag groups
                e.g. [['forward', 'fp16'], ['backward', 'fp32']]
                this option is mutually exclusive with group_tag_cartesian
            tag_display_mode: 'column' or 'concat'
            tag_headers: only useful if display_tag_mode=='column'
        """
        assert tag_display_mode in ["concat", "column"]
        self.warmup_tests = [c for c in test_cases if c._is_warmup]
        self.normal_tests = [c for c in test_cases if not c._is_warmup]
        assert self.warmup_tests or self.normal_tests, "must have at least one test"
        if randomize:
            random.shuffle(self.normal_tests)

        if tag_headers is None:
            tag_headers = []
        assert isinstance(tag_headers, (list, tuple))
        self._tag_headers = tag_headers

        assert group_tag_flat or group_tag_cartesian, "mutually exclusive"
        self._check_list_of_list(group_tag_flat)
        self._check_list_of_list(group_tag_cartesian)
        self._group_tag_flat = group_tag_flat
        self._tag_groups = []
        if group_tag_flat:
            self._tag_groups = group_tag_flat
            assert all(
                len(v) == len(self._tag_groups[0]) for v in self._tag_groups
            ), "all tag groups must have the same number of tags"
        self._group_tag_cartesian = group_tag_cartesian
        self._tag_groups = []  # filled by either group_tag_flat or .._cartesian
        self._tag_display_mode = tag_display_mode
        self._table = []
        self._verbose = verbose
        self.run()

    def _check_list_of_list(self, value):
        if value is not None and value != "auto":
            assert isinstance(value, (list, tuple))
            assert all(isinstance(v, (list, tuple)) for v in value)

    def _run_case(self, case):
        assert isinstance(case, TestCase)
        case._run(self._verbose)
        if not case._is_warmup:
            self._table.append(
                (
                    case.name,
                    case.tags,
                    (case._avg_best, case._avg_total, case._min, case._max),
                )
            )

    def _generate_cartesian(self):
        if self._group_tag_cartesian:
            if self._group_tag_cartesian == "auto":
                all_tags = [entry[1] for entry in self._table]
                choices = list(map(tuple, map(U.OrderedSet, zip(*all_tags))))
            else:
                choices = self._group_tag_cartesian
            self._tag_groups = list(itertools.product(*choices))

    def run(self):
        for case in self.warmup_tests + self.normal_tests:
            self._run_case(case)

        if self._verbose:
            print("*" * 40, "\n")

        self._generate_cartesian()

        # all tags are tuples
        table_groups = OrderedDict()
        for tags in self._tag_groups:
            table_groups[tuple(tags)] = []
        table_groups[None] = []  # catch the rest

        while self._table:
            name, tags, stats = self._table.pop(0)
            entry = []
            name_and_tag = [name, *tags]
            if self._tag_display_mode == "concat":
                entry.append("_".join(name_and_tag))
            elif self._tag_display_mode == "column":
                entry.extend(name_and_tag)
            entry.extend(stats)
            if tags in table_groups:
                table_groups[tags].append(entry)
            else:
                table_groups[None].append(entry)
            # if the entry's tags are a subset of one of table_group's tag group
            # for tag_group in table_groups:
            #     if tag_group and set(tag_group) in set(tags):
            #         table_groups[tag_group].append(entry)
            #         break
            # else:
            #     table_groups[None].append(entry)

        table_rows = []
        for tags, entries in table_groups.items():
            if not entries:  # keyword corresponds to nothing
                continue
            entries.sort()
            table_rows.extend(entries)
            # separator
            table_rows.append("__SEP__")
        table_rows.pop()
        # make separator same width as table
        max_widths = [0] * len(entry)
        for entry in table_rows:
            if entry == "__SEP__":
                continue
            for i, e in enumerate(entry):
                max_widths[i] = max(max_widths[i], len(e))
        for i, entry in enumerate(table_rows):
            if entry == "__SEP__":
                table_rows[i] = ("-" * width for width in max_widths)

        tag_headers = self._tag_headers[: len(entry) - 5]

        print(
            tabulate(
                table_rows,
                headers=[
                    "Run",
                    *tag_headers,
                    "avg (BEST)",
                    "avg (TOTAL)",
                    "min",
                    "max",
                ],
                tablefmt="presto",
            )
        )
