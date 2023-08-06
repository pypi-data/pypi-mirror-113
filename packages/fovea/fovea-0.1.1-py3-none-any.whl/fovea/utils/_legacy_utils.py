# FIXME

import sys
import os
import inspect
import collections
import functools
import re
import pprint
import string
import collections.abc
from enum import Enum, EnumMeta


class DotDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    __reduce__ = lambda self: (dict, (), None, None, iter(self.items()))


class DotDictRef:
    """
    Dot-accessible reference to a dictionary data
    """

    def __new__(cls, data):
        def _getattr(self, key):
            if key in data:
                return data[key]
            else:
                raise AttributeError("key {} does not exist".format(key))

        cls.__getattr__ = _getattr
        cls.__setattr__ = data.__setitem__
        cls.__setattr__ = data.__setitem__
        cls.__delattr__ = data.__delitem__
        cls.__getitem__ = data.__getitem__
        cls.__setitem__ = data.__setitem__
        cls.__delitem__ = data.__delitem__
        cls.__contains__ = data.__contains__
        # make pickleable
        cls.__reduce__ = lambda self: (dict, (), None, None, iter(data.items()))
        cls.__repr__ = data.__repr__
        return super().__new__(cls)


def show_set_diff(data1, data2, name1=None, name2=None):
    if not name1:
        name1 = "set#1"
    if not name2:
        name2 = "set#2"
    data1, data2 = set(data1), set(data2)
    if data1 - data2:
        print(f"Keys in {name1} but not in {name2}: ", list(data1 - data2))
    if data2 - data1:
        print(f"Keys in {name2} but not in {name1}: ", list(data2 - data1))


def _get_qualified_type_name(type_):
    name = str(type_)
    r = re.compile("<class '(.*)'>")
    match = r.match(name)
    if match:
        return match.group(1)
    else:
        return name


def assert_type(x, expected_type, message=""):
    assert isinstance(x, expected_type), (
        message + ": " if message else ""
    ) + "expected type `{}`, actual type `{}`".format(
        _get_qualified_type_name(expected_type), _get_qualified_type_name(type(x))
    )
    return True


def _pformat(obj, **pformat_kwargs):
    "only pformat collections.abc.Container"
    if isinstance(obj, collections.abc.Container) and not isinstance(obj, str):
        indent = pformat_kwargs.pop("indent", 4)  # default indent 4
        return pprint.pformat(obj, indent=indent, **pformat_kwargs)
    else:
        return obj


def prettyprint(*objs, **pformat_kwargs):
    "apply pprint.pformat to only collections.abc.Container"
    objs = [_pformat(o) for o in objs]
    print(*objs, **pformat_kwargs)


def print_debug(*objs, h="", **pformat_kwargs):
    """
    Args:
      *objs: objects to be pretty-printed
      h: header string
      **kwargs: other kwargs to pass on to ``pprint()``
    """
    if h:
        print("=" * 20, h, "=" * 20)
    prettyprint(*objs, **pformat_kwargs)
    if h:
        print("=" * (42 + len(h)))


def print_multiprocess(
    *objs,
    all_prefix="=>",
    master_prefix=None,
    worker_prefix="<{}>",
    process_rank,
    broadcast,
    pretty_format=True,
    print_method=None,
    **print_kwargs,
):
    """
    Used in distributed WorkerManager and Session API

    Args:
        all_prefix (default '=>')
        master_prefix (default None): only active with broadcast=True,
        worker_prefix (default '<{}>'): worker_prefix.format(rank)
        pretty_format (default True): use pprint.pformat
        broadcast (default False): all worker processes print to stdout
    """
    is_master = process_rank == 0
    if not is_master and not broadcast:
        return  # print nothing
    if print_method is None:
        print_method = print

    prefix = all_prefix
    space = " " if all_prefix.strip() else ""
    if master_prefix is None:
        master_prefix = worker_prefix.format(0)
    if is_master:
        if master_prefix and broadcast:
            prefix += space + master_prefix
    else:  # worker
        if not worker_prefix:
            pass
        elif isinstance(worker_prefix, str):
            prefix += space + worker_prefix.format(process_rank)
        else:
            raise ValueError(
                "worker_prefix must be a formatting str, worker_prefix.format(rank: int)"
            )
    if pretty_format:
        objs = [_pformat(o) for o in objs]

    return print_method(prefix, *objs, **print_kwargs)


def printfmt_multiprocess(
    fmt_str,
    *fmt_args,
    all_prefix="=>",
    master_prefix=None,
    worker_prefix="<{}>",
    process_rank,
    broadcast,
    pretty_format=True,
    print_method=None,
    **fmt_kwargs,
):

    if pretty_format:
        fmt_args = [_pformat(o) for o in fmt_args]
        fmt_kwargs = {name: _pformat(value) for name, value in fmt_kwargs.items()}
    s = fmt_str.format(*fmt_args, **fmt_kwargs)
    return print_multiprocess(
        s,
        all_prefix=all_prefix,
        master_prefix=master_prefix,
        worker_prefix=worker_prefix,
        process_rank=process_rank,
        broadcast=broadcast,
        pretty_format=False,
        print_method=print_method,
    )


def get_print_multiprocess_options(option_dict):
    if not option_dict:
        option_dict = {}
    defaults = {
        "all_prefix": "=>",
        "master_prefix": None,
        "worker_prefix": "<{}>",
        "pretty_format": True,
        "broadcast": False,
    }
    defaults.update(option_dict)  # overwrite any defaults with values in option
    return defaults


class _GetItemEnumMeta(EnumMeta):
    """
    Hijack the __getitem__ method from metaclass, because subclass cannot
        override magic methods. More informative error message.
    """

    def __getitem__(self, option):
        enum_class = None
        for v in self.__members__.values():
            enum_class = v.__class__
            break
        assert enum_class is not None, "must have at least one option in StringEnum"
        return get_enum(enum_class, option)


class StringEnum(Enum, metaclass=_GetItemEnumMeta):
    """
    https://docs.python.org/3.4/library/enum.html#duplicatefreeenum
    The created options will automatically have the same string value as name.

    Support [] subscript, i.e. MyFruit['orange'] -> MyFruit.orange
    """

    def __init__(self, *args, **kwargs):
        self._value_ = self.name


def create_string_enum(class_name, option_names):
    assert_type(option_names, str)
    assert_type(option_names, list)
    return StringEnum(class_name, option_names)


def get_enum(enum_class, option):
    """
    Args:
        enum_class:
        option: if the value doesn't belong to Enum, throw error.
            Can be either the str name or the actual enum value
    """
    assert issubclass(enum_class, StringEnum)
    if isinstance(option, enum_class):
        return option
    else:
        assert_type(option, str)
        option = option.lower()
        options = enum_class.__members__
        if option not in options:
            raise ValueError(
                '"{}" is not a valid option for {}. '
                "Available options are {}.".format(
                    option, enum_class.__name__, list(options)
                )
            )
        return options[option]


def fformat(float_num, precision):
    """
    https://stackoverflow.com/a/44702621/3453033
    """
    assert isinstance(precision, int) and precision > 0
    return "{{:.{}f}}".format(precision).format(float_num).rstrip("0").rstrip(".")


def make_tuple(elem, repeats):
    """
    E.g. expand 3 into (3, 3) for things like strides/paddings
    """
    if isinstance(elem, int):
        return [elem] * repeats
    else:
        assert len(elem) == repeats
        return [int(x) for x in elem]


def iter_last(iterable):
    """
    For processing the last element differently
    Yields: (is_last=bool, element)
    """
    length = len(iterable)
    return ((i == length - 1, x) for i, x in enumerate(iterable))


def merge_dicts(*dicts, descending_priority=True):
    """
    Merge all dicts into a single new dict.
    Args:
        descending_priority: deals with duplicate key.
            from left (earlier) to right (later) dict args,
            if True, the earlier dicts' duplicate key will override later dicts.
    """
    for d in dicts:
        assert isinstance(d, dict)
    if descending_priority:
        dicts = reversed(dicts)
    D = {}
    for d in dicts:
        D.update(d)
    return D


def parse_formatter_vars(format_str):
    """
    Returns:
        list of all variables that appear in the format string
        e.g. '{foo:.2f} has {bar:>5s}' returns ['foo'], ['bar']
    """
    names = []
    for _, name, fmt, _ in string.Formatter().parse(format_str):
        # the last fmt is always None with no corresponding name
        if fmt is not None:
            names.append(name)
    return names


def case_insensitive_match(items, key):
    """
    Args:
        items: iterable of keys
        key: search for the key case-insensitively

    Returns:
        matched original key (with cases), None if no match
    """
    for k in items:
        if k.lower() == key.lower():
            return k
    return None


def _to_float(x):
    # make an attempt to convert to plain float. If fails, just keep original
    if isinstance(x, int):
        return x
    try:
        return float(x)
    except (ValueError, TypeError):
        return x


def to_float_dict(d):
    "recursive"
    newd = {}
    for k, v in d.items():
        if isinstance(v, dict):
            newd[k] = to_float_dict(v)
        else:
            newd[k] = _to_float(v)
    return newd


def _get_bound_args(func, *args, **kwargs):
    """
    https://docs.python.org/3/library/inspect.html#inspect.BoundArguments
    def f(a, b, c=5, d=6): pass
    get_bound_args(f, 3, 6, d=100) -> {'a':3, 'b':6, 'c':5, 'd':100}

    Returns:
        OrderedDict of bound arguments
    """
    arginfo = inspect.signature(func).bind(*args, **kwargs)
    arginfo.apply_defaults()
    return arginfo.arguments


class _Deprecated_SaveInitArgsMeta(type):
    """
    Bounded arguments:
    https://docs.python.org/3/library/inspect.html#inspect.BoundArguments

    Store the captured constructor arguments to <instance>._init_args_dict
    as OrderedDict. Can be retrieved by the property method <obj>.init_args_dict
    Includes both the positional args (with the arg name) and kwargs
    """

    def __init__(cls, name, bases, attrs):
        # WARNING: must add class method AFTER super.__init__
        # adding attrs['new-method'] before __init__ has no effect!
        super().__init__(name, bases, attrs)

        @property
        def init_args_dict(self):
            return self._init_args_dict

        cls.init_args_dict = init_args_dict

    def __call__(cls, *args, **kwargs):
        obj = super().__call__(*args, **kwargs)
        try:
            obj._init_args_dict = _get_bound_args(obj.__init__, *args, **kwargs)
        except TypeError:  # __init__ has special stuff like *args
            obj._init_args_dict = None
        return obj


class SaveInitArgsMeta(type):
    """
    Store __init__ call args in self.init_args_dict
    Positional args to __init__ will be stored under `None` key
    Keyword args to __init__ will be stored as-is in init_args_dict
    """

    def __init__(cls, name, bases, attrs):
        # WARNING: must add class method AFTER super.__init__
        # adding attrs['new-method'] before __init__ has no effect!
        super().__init__(name, bases, attrs)

        @property
        def init_args_dict(self):
            return self._init_args_dict

        cls.init_args_dict = init_args_dict

    def __call__(cls, *args, **kwargs):
        obj = super().__call__(*args, **kwargs)
        init_dict = {}
        if args:
            init_dict[None] = list(args)  # convert to list for YAML compatibility
        init_dict.update(kwargs)
        obj._init_args_dict = init_dict
        return obj


class SaveInitArgs(metaclass=SaveInitArgsMeta):
    """
    Either use metaclass hook:
        class MyObj(metaclass=SaveInitArgsMeta)
    or simply inherit
        class MyObj(SaveInitArgs)
    """

    pass


class AutoInitializeMeta(type):
    """
    Call the special method ._initialize() after __init__.
    Useful if some logic must be run after the object is constructed.
    For example, the following code doesn't work because `self.y` does not exist
    when super class calls self._initialize()

    class BaseClass():
        def __init__(self):
            self._initialize()

        def _initialize():
            self.x = self.get_x()

        def get_x(self):
            # abstract method that only subclass

    class SubClass(BaseClass):
        def __init__(self, y):
            super().__init__()
            self.y = y

        def get_x(self):
            return self.y * 3

    Fix:
    class BaseClass(metaclass=AutoInitializeMeta):
        def __init__(self):
            pass
            # self._initialize() is now automatically called after __init__

        def _initialize():
            print('INIT', self.x)

        def get_x(self):
            # abstract method that only subclass
            raise NotImplementedError
    """

    def __call__(self, *args, **kwargs):
        obj = super().__call__(*args, **kwargs)
        assert hasattr(
            obj, "_initialize"
        ), "AutoInitializeMeta requires that subclass implements _initialize()"
        obj._initialize()
        return obj


class SerializedDict:
    def __init__(self, keys):
        self.keys = keys

    def dump(self):
        return {key: getattr(self, key) for key in self.keys}

    def load(self, state_dict):
        for key in self.keys:
            assert key in state_dict, 'Loading error: key "{}" missing'.format(key)
            setattr(self, key, state_dict[key])
        return self


class noop_context:
    """
    Placeholder context manager that does nothing.
    We could have written simply as:

    @contextmanager
    def noop_context(*args, **kwargs):
        yield

    but the returned context manager cannot be called twice, i.e.
    my_noop = noop_context()
    with my_noop:
        do1()
    with my_noop: # trigger generator error
        do2()
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def meta_wrap(decor):
    """
    a decorator decorator, allowing the wrapped decorator to be used as:
    @decorator(*args, **kwargs)
    def callable()
      -- or --
    @decorator  # without parenthesis, args and kwargs will use default
    def callable()

    Args:
      decor: a decorator whose first argument is a callable (function or class
        to be decorated), and the rest of the arguments can be omitted as default.
        decor(f, ... the other arguments must have default values)

    Warning:
      decor can NOT be a function that receives a single, callable argument.
      See stackoverflow: http://goo.gl/UEYbDB
    """
    single_callable = (
        lambda args, kwargs: len(args) == 1 and len(kwargs) == 0 and callable(args[0])
    )

    @functools.wraps(decor)
    def new_decor(*args, **kwargs):
        if single_callable(args, kwargs):
            # this is the double-decorated f.
            # It should not run on a single callable.
            return decor(args[0])
        else:
            # decorator arguments
            return lambda real_f: decor(real_f, *args, **kwargs)

    return new_decor


@meta_wrap
def deprecated(func, msg="", action="warning"):
    """
    Function/class decorator: designate deprecation.

    Args:
      msg: string message.
      action: string mode
      - 'warning': (default) prints `msg` to stderr
      - 'noop': do nothing
      - 'raise': raise DeprecatedError(`msg`)
    """
    action = action.lower()
    if action not in ["warning", "noop", "raise"]:
        raise ValueError("unknown action type {}".format(action))
    if not msg:
        msg = "This is a deprecated feature."

    # only does the deprecation when being called
    @functools.wraps(func)
    def _deprecated(*args, **kwargs):
        if action == "warning":
            print(msg, file=sys.stderr)
        elif action == "raise":
            raise DeprecationWarning(msg)
        return func(*args, **kwargs)

    return _deprecated


def pack_varargs(args):
    """
    Pack *args or a single list arg as list

    def f(*args):
        arg_list = pack_varargs(args)
        # arg_list is now packed as a list
    """
    assert isinstance(args, tuple), "please input the tuple `args` as in *args"
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        return args[0]
    else:
        return args


def enable_list_arg(func):
    """
    Function decorator.
    If a function only accepts varargs (*args),
    make it support a single list arg as well
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args = pack_varargs(args)
        return func(*args, **kwargs)

    return wrapper


def enable_varargs(func):
    """
    Function decorator.
    If a function only accepts a list arg, make it support varargs as well
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args = pack_varargs(args)
        return func(args, **kwargs)

    return wrapper


def pack_kwargs(args, kwargs):
    """
    Pack **kwargs or a single dict arg as dict

    def f(*args, **kwargs):
        kwdict = pack_kwargs(args, kwargs)
        # kwdict is now packed as a dict
    """
    if len(args) == 1 and isinstance(args[0], dict):
        assert not kwargs, "cannot have both **kwargs and a dict arg"
        return args[0]  # single-dict
    else:
        assert not args, "cannot have positional args if **kwargs exist"
        return kwargs


def enable_dict_arg(func):
    """
    Function decorator.
    If a function only accepts varargs (*args),
    make it support a single list arg as well
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        kwargs = pack_kwargs(args, kwargs)
        return func(**kwargs)

    return wrapper


def enable_kwargs(func):
    """
    Function decorator.
    If a function only accepts a dict arg, make it support kwargs as well
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        kwargs = pack_kwargs(args, kwargs)
        return func(kwargs)

    return wrapper


def method_decorator(decorator):
    """
    Decorator of decorator: transform a decorator that only works on normal
    functions to a decorator that works on class methods
    From Django form: https://goo.gl/XLjxKK
    """

    @functools.wraps(decorator)
    def wrapped_decorator(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            def bound_func(*args2, **kwargs2):
                return method(self, *args2, **kwargs2)

            return decorator(bound_func)(*args, **kwargs)

        return wrapper

    return wrapped_decorator


def accepts_varargs(func):
    """
    If a function accepts *args
    """
    params = inspect.signature(func).parameters
    return any(
        param.kind == inspect.Parameter.VAR_POSITIONAL for param in params.values()
    )


def accepts_kwargs(func):
    """
    If a function accepts **kwargs
    """
    params = inspect.signature(func).parameters
    return any(param.kind == inspect.Parameter.VAR_KEYWORD for param in params.values())


def is_signature_compatible(func, *args, **kwargs):
    sig = inspect.signature(func)
    try:
        sig.bind(*args, **kwargs)
        return True
    except TypeError:
        return False


class OrderedSet(collections.abc.MutableSet):
    """
    Recommended recipe from official python:
    https://code.activestate.com/recipes/576694/
    """

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]  # sentinel node for doubly linked list
        self.map = {}  # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError("set is empty")
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return "%s()" % (self.__class__.__name__,)
        return "%s(%r)" % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)
