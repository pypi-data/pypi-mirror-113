"""
https://pytorch.org/docs/stable/distributed.html
https://pytorch.org/docs/stable/data.html#torch.utils.data.distributed.DistributedSampler
https://pytorch.org/docs/stable/distributed.html#launch-utility

Complete working example:
https://github.com/pytorch/examples/blob/master/imagenet/main.py

Wrapper around nn.DataParallel and nn.parallel.DistributedDataParallel
"""
import collections
import os
import copy
import random
import numpy as np
import torch
import torch.nn as nn
import torch.distributed as dist
import torch.multiprocessing as mp
import torch.utils.data
import omlet.utils as U
from .manager import WorkerManager
from .utils import *


__all__ = [
    "DistLauncher",
    "ReplicaDistLauncher",
    "LocalDistLauncher",
    "DPLauncher",
    "SingleGPULauncher",
]

# https://discuss.pytorch.org/t/issue-with-multiprocessing-semaphore-tracking/22943/4
os.environ["PYTHONWARNINGS"] = "ignore:semaphore_tracker:UserWarning"


class DistLauncher:
    def __init__(
        self,
        *,
        world_size,
        url="env://",
        backend="nccl",
        gpu_indices=None,
        global_rank_offset=0,
        process_group_size=0,
        process_group_lists=None,
        use_nvidia_apex=False,
        print_options=None,
    ):
        """
        Args:
            url: defaults to env://. Replace localhost with 127.0.0.1
            backend: nccl, gloo, mpi, tcp
            process_group_size: mutually exclusive with `process_group_lists`
                divide all processes into groups with the same size.
                Only useful with DDP modes
            process_group_lists: must be a list of list of process global rank,
                e.g. [[0,1,2,3], [4,7], [5,6,8]]
                mutually exclusive with `process_group_size`
                Only useful with DDP modes
            print_options: a dict of options specific to print
                all_prefix (default '=>')
                master_prefix (default None): only active with broadcast=True,
                worker_prefix (default '<{}>'): worker_prefix.format(rank)
                pretty_format (default True): use pprint.pformat
                broadcast (default False): all worker processes print to stdout
        """
        if "//" not in url:
            url = "tcp://" + url
        url = url.replace("localhost", "127.0.0.1")
        self.url = url
        self.backend = backend
        if not gpu_indices:  # take all GPUs
            num_gpus = self.get_device_count()
            assert num_gpus > 0, "no GPUs found"
            gpu_indices = list(range(num_gpus))
        else:
            assert (
                isinstance(gpu_indices, collections.abc.Sequence)
                and len(gpu_indices) > 0
            ), f'invalid gpu_indices "{gpu_indices}"'
        self.gpu_indices = list(gpu_indices)
        self.world_size = world_size
        self.global_rank_offset = global_rank_offset
        # FIXME: print options
        self.print_options = U.get_print_multiprocess_options(print_options)

        self.use_nvidia_apex = use_nvidia_apex
        if self.use_nvidia_apex:
            assert has_nvidia_apex(), "Nvidia apex is not installed"
            assert backend == "nccl", "Nvidia apex only works with NCCL backend"

        assert not (
            process_group_size and process_group_lists
        ), "process_group_lists and process_group_size are mutually exclusive"
        self.process_group_lists = None
        if process_group_lists or process_group_size:
            assert self.is_ddp(), "process groups are only used under DDP modes"
            if process_group_lists:
                assert isinstance(process_group_lists, (list, tuple))
                # disallow overlapping groups
                gset = set()
                for pg in process_group_lists:
                    assert isinstance(
                        pg, (list, tuple)
                    ), "process_group_lists must be a list of list of process global rank"
                    assert pg, "process group must not be empty"
                    assert len(pg) == len(
                        set(pg)
                    ), "one group cannot have duplicate processes"
                    overlap = gset & set(pg)
                    assert (
                        len(overlap) == 0
                    ), 'processes "{}" cannot repeat across multiple groups'.format(
                        overlap
                    )
                    gset.update(pg)
                self.process_group_lists = process_group_lists
            else:
                # expand process_group_size into process_group_lists
                # e.g. size=2 with world_size=8: [[0,1],[2,3],[4,5],[6,7]]
                assert process_group_size > 0, "process_group_size must be positive"
                assert (
                    world_size % process_group_size == 0
                ), "process_group_size must divide world_size"
                self.process_group_lists = []
                pgs = process_group_size
                for i in range(world_size // pgs):
                    self.process_group_lists.append(list(range(i * pgs, (i + 1) * pgs)))

    @property
    def mode(self):
        """
        ddp: DistributedDataParallel
        dp: DataParallel
        single: single GPU training
        """
        if self.world_size > 0:
            if self.use_nvidia_apex:
                return "ddp_apex"
            else:
                return "ddp"
        elif len(self.gpu_indices) == 1:
            return "single"
        else:
            return "dp"

    def is_ddp(self):
        return self.mode in ["ddp", "ddp_apex"]

    @property
    def num_gpus(self):
        return len(self.gpu_indices)

    def get_device_count(self):
        return torch.cuda.device_count()

    def launch(self, worker_func, *worker_args, **worker_kwargs):
        """
        TODO: make this a decorator?

        Only run this in the master process. Will block until the processes exit.
        Args:
            worker_func: callable, needs to create a DistributedManager object
            and call `worker_entry()` function
        """
        if self.is_ddp():
            mp.spawn(
                self._worker_wrapper,
                nprocs=self.num_gpus,
                args=(worker_func, worker_args, worker_kwargs),
                join=True,
            )
        else:
            # simply run in the main thread
            self._worker_wrapper(
                local_rank=0,
                worker_func=worker_func,
                worker_args=worker_args,
                worker_kwargs=worker_kwargs,
            )

    def launch_async(self, worker_func, *worker_args, **worker_kwargs):
        """
        Non-blocking version of launch()

        Returns:
            torch.multiprocessing.SpawnContext, returns control immediately
        """
        if self.is_ddp():
            nprocs = self.num_gpus
        else:
            nprocs = 1
        # join=False to be non-blocking
        return mp.spawn(
            self._worker_wrapper,
            nprocs=nprocs,
            args=(worker_func, worker_args, worker_kwargs),
            join=False,
        )

    def _worker_wrapper(self, local_rank, worker_func, worker_args, worker_kwargs):
        global_rank = self.global_rank_offset + local_rank
        group = None
        group_ids = None
        if self.is_ddp():
            dist.init_process_group(
                backend=self.backend,
                init_method=self.url,
                world_size=self.world_size,
                rank=global_rank,
            )
            # all procs must reach `new_group()` call even when they don't belong
            if self.process_group_lists:
                for gids in self.process_group_lists:
                    g = dist.new_group(gids, backend=self.backend)
                    # if multiple groups share the same process, we only assign
                    # the process to the first group in which it appears
                    if global_rank in gids and group is None:
                        group = g
                        group_ids = gids
        if group is None:
            group = WorkerManager.DEFAULT_GROUP

        # set globally accessible env variable
        # can be read by get_local_rank()
        os.environ["TORCHX_LOCAL_RANK"] = str(local_rank)
        os.environ["TORCHX_GLOBAL_RANK"] = str(global_rank)
        os.environ["TORCHX_WORLD_SIZE"] = str(self.world_size)

        manager = WorkerManager(
            local_rank=local_rank,
            global_rank=global_rank,
            world_size=self.world_size,
            gpu_indices=self.gpu_indices,
            mode=self.mode,
            backend=self.backend,
            group=group,
            group_ids=group_ids,
            print_options=self.print_options,
        )
        with manager.device_context():
            worker_func(manager, *worker_args, **worker_kwargs)


def ReplicaDistLauncher(
    *,
    node_index,
    num_nodes,
    num_gpus=-1,
    gpu_indices=None,
    url="env://",
    backend="nccl",
    process_group_size=0,
    process_group_lists=None,
    use_nvidia_apex=False,
    print_options=None,
):
    """
    ReplicaDistLauncher assumes that each node has the same number of GPUs

    TODO: use lightning-style GPU spec:
        "2": 2 GPUs
        "-1" or "all"
        "3,4,5,6"
        [3, 4, 5, 6]
    """
    if gpu_indices is None:
        if num_gpus <= 0:
            num_gpus = torch.cuda.device_count()
        assert num_gpus > 0, "no GPU found"
        gpu_indices = list(range(num_gpus))
    else:
        assert num_gpus == -1, (
            "num_gpus and gpu_indices are mutually exclusive. "
            "If gpu_indices is specified, num_gpus must be -1."
        )
        assert (
            isinstance(gpu_indices, collections.abc.Sequence) and len(gpu_indices) > 0
        ), f'invalid gpu_indices "{gpu_indices}"'
    num_gpus = len(gpu_indices)

    return DistLauncher(
        world_size=num_nodes * num_gpus,
        url=url,
        backend=backend,
        gpu_indices=gpu_indices,
        global_rank_offset=node_index * num_gpus,
        process_group_size=process_group_size,
        process_group_lists=process_group_lists,
        use_nvidia_apex=use_nvidia_apex,
        print_options=print_options,
    )


def LocalDistLauncher(
    port,
    num_gpus=-1,
    gpu_indices=None,
    process_group_size=0,
    process_group_lists=None,
    backend="nccl",
    use_nvidia_apex=False,
    print_options=None,
):
    return ReplicaDistLauncher(
        node_index=0,
        num_nodes=1,
        num_gpus=num_gpus,
        gpu_indices=gpu_indices,
        url=f"tcp://127.0.0.1:{port}",
        process_group_size=process_group_size,
        process_group_lists=process_group_lists,
        backend=backend,
        use_nvidia_apex=use_nvidia_apex,
        print_options=print_options,
    )


def DPLauncher(gpu_indices=None, backend="nccl", print_options=None):
    return DistLauncher(
        world_size=0,
        gpu_indices=gpu_indices,
        backend=backend,
        print_options=print_options,
    )


def SingleGPULauncher(gpu_index=0, print_options=None):
    return DistLauncher(
        world_size=0, gpu_indices=[gpu_index], print_options=print_options
    )
