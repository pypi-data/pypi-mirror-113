import collections
import contextlib

import torch
import pprint
import numpy as np
import fnmatch
from typing import Any, List, Union, Optional, Dict, Callable, Tuple
import omlet.utils as U


class DataDict(collections.abc.Mapping):
    _PROTECTED_METHODS = [
        # basic dict-like methods
        "keys",
        "values",
        "items",
        "get",
        "pop",
        "update",
        "settings",
        "Immutable",
        # functional transforms
        "to_dict",
        "to_numpy",
        "to_tensor",
        "map",
        "multi_map",
        "traverse",
        "multi_traverse",
        # type methods
        "is_array",
        "is_primitive_array",
        "is_advanced_array",  # supports advanced indexing: np.ndarray and torch.Tensor
        "is_mapping",
        "is_immutable",
        "is_sliceable",
    ]

    class Immutable:
        """
        Use this wrapper to prevent DataDict from converting the dict content into DataDict
        recursively or index into an np.ndarray/torch.Tensor. For example:

        b = DataDict()
        b.obs = {'rgb': 1, 'sensor': 2}  # b.obs will become another DataDict structure
        b.obs = DataDict.Immutable({'rgb': 1, 'sensor': 2})  # b.obs will remain a primitive dict
                    # b.obs.rgb will NOT work, you have to use b.obs['rgb']
        b.sensor = np.ndarray([1,2,3])
        b[:2]  # will index into b.sensor
        b.sensor = DataDict.Immutable(np.ndarray([1,2,3]))
        b[:2]  # will not index b.sensor and will return it as-is
        """

        def __init__(self, data):
            self.data = data

        def __repr__(self):
            return "<immu> " + repr(self.data)

    _DEFAULT_SETTINGS = {
        # b[:2] will index into primitive sequence like list and tuple
        # by default, only np.ndarray and torch.Tensor supports indexing
        "index_primitive_sequence": True,
        # if True, b[2:5] = other_b will check for keys in other_b that don't exist in b
        "strict_assign": True,
    }

    # controls global setting
    _settings = _DEFAULT_SETTINGS.copy()

    def __init__(self, _data_: collections.abc.Mapping = None, **kwargs):
        """
        Args:
            DataDict(mapping) positional only
            or DataDict(**kwargs)
        """
        self._internal_keys = []
        if _data_ is not None:
            assert not kwargs, (
                "DataDict can only be constructed by either a single "
                "positional arg (of type Mapping) or **kwargs, but not both"
            )
            if isinstance(_data_, self.__class__):
                items = _data_._wrapped_items()
            else:
                items = _data_.items()
        else:
            items = kwargs.items()

        for k, v in items:
            self[k] = v

    def to_dict(self):
        """
        Convert to primitive dict
        """
        return {
            k: v.to_dict() if isinstance(v, DataDict) else v for k, v in self.items()
        }

    @staticmethod
    def is_array(obj):
        return DataDict.is_primitive_array(obj) or DataDict.is_advanced_array(obj)

    @staticmethod
    def is_primitive_array(obj):
        return isinstance(obj, collections.abc.MutableSequence)

    @staticmethod
    def is_advanced_array(obj):
        return isinstance(obj, (np.ndarray, torch.Tensor))

    @staticmethod
    def is_mapping(obj):
        return isinstance(obj, collections.abc.Mapping)

    @classmethod
    def is_immutable(cls, obj):
        """
        Neither sequence nor mapping.
        If `index_primitive_sequence` is False, python list is also considered immutable.
        """
        return not cls.is_sliceable(obj) and not DataDict.is_mapping(obj)

    @classmethod
    def is_sliceable(cls, obj):
        if cls._settings["index_primitive_sequence"]:
            return cls.is_array(obj)
        else:
            return cls.is_advanced_array(obj)

    @staticmethod
    def _is_private(name):
        return name.startswith("_")

    @classmethod
    def settings(cls, **kwargs):
        """
        Any None will be ignored
        """
        if kwargs.pop("reset", False):
            cls._settings = cls._DEFAULT_SETTINGS.copy()
        for k, v in kwargs.items():
            assert k in cls._DEFAULT_SETTINGS, f"setting {k} is not supported."
            if v is not None:
                cls._settings[k] = v

    @classmethod
    @contextlib.contextmanager
    def settings_scope(cls, **kwargs):
        old_settings = cls._settings.copy()
        cls.settings(**kwargs)
        yield
        cls._settings = old_settings

    @staticmethod
    def _unwrap_immutable(x):
        return x.data if isinstance(x, DataDict.Immutable) else x

    def __getattribute__(self, name):
        """
        WARNING: __getattr__ only gets called every time an attribute is missing
            __getattribute__ gets called every time an attribute is *accessed*
        """
        if DataDict._is_private(name) or name in DataDict._PROTECTED_METHODS:
            return object.__getattribute__(self, name)
        else:
            try:
                return self.__getitem__(name)
            except KeyError as e:
                raise AttributeError(str(e))

    def __setattr__(self, name, value):
        if DataDict._is_private(name):
            return object.__setattr__(self, name, value)
        else:
            try:
                self.__setitem__(name, value)
            except KeyError as e:
                raise AttributeError(str(e))

    def __delattr__(self, name):
        if name in DataDict._PROTECTED_METHODS:
            raise AttributeError(f"{name} is a protected method, cannot be deleted")
        elif DataDict._is_private(name):
            raise AttributeError(f"{name} is a private attribute, cannot be deleted")
        else:
            try:
                self.__delitem__(name)
            except KeyError as e:
                raise AttributeError(str(e))

    def __getitem__(self, index: Union[str, slice]):
        if isinstance(index, str):
            if "." in index:
                parent_key, child_key = index.split(".", 1)
                # recurse through every `.`
                return self[parent_key][child_key]
            else:  # base case, key does not have "."
                if index not in self._internal_keys:
                    raise KeyError(f"Missing key {index}")
                ret = self.__dict__[index]
                return self._unwrap_immutable(ret)

        else:  # array slicing
            ret = DataDict()
            for k, v in self._wrapped_items():
                if self.is_immutable(v):
                    # primitive type cannot be index-sliced
                    ret[k] = v
                elif self.is_primitive_array(v):
                    assert self._settings["index_primitive_sequence"], (
                        "INTERNAL, should have been handled by "
                        "self._is_immutable() already"
                    )
                    # support advanced indexing into list
                    v_slice = np.array(v, dtype=np.object)[index]
                    ret[k] = type(v)(v_slice)
                else:
                    # ndarray and tensor
                    ret[k] = v[index]
            return ret

    def __setitem__(self, index: str, value):
        if isinstance(index, str):
            if "." in index:
                parent_key, child_key = index.split(".", 1)
                if parent_key not in self:
                    self[parent_key] = DataDict()
                # recurse through every `.`
                self[parent_key][child_key] = value
            else:  # base case, key does not have "."
                if index in DataDict._PROTECTED_METHODS:
                    raise KeyError(
                        f"{index} is a protected method, cannot be overridden"
                    )
                elif DataDict._is_private(index):
                    raise KeyError(f"DataDict keys must not start with '_'")
                if (
                    DataDict.is_mapping(value)
                    # we don't deepcopy item that's already DataDict
                    and not isinstance(value, DataDict)
                ):
                    self.__dict__[index] = DataDict(value)
                else:
                    self.__dict__[index] = value
                if index not in self._internal_keys:
                    self._internal_keys.append(index)

        else:  # array slicing
            assert self.is_mapping(value), (
                f"assignment {value} must be a mapping that "
                f"partially matches the structure of this DataDict object"
            )
            if not isinstance(value, DataDict):
                value = DataDict(value)
            self._check_same_struct(value, prefix="")
            for k, assign in value._wrapped_items():
                if k in self.keys():
                    ours = self[k]
                    assign = self._unwrap_immutable(assign)
                    # support advanced indexing into list
                    if self.is_primitive_array(ours):
                        ours = np.array(ours, dtype=np.object)
                        ours.__setitem__(index, assign)
                        self[k] = ours
                    else:
                        # if it's a sequence, then assign the value to the slice portion
                        # if it's another DataDict, recurse
                        self[k].__setitem__(index, assign)

    def __delitem__(self, key):
        assert isinstance(key, str), "only string key deletion is supported"
        if "." in key:
            parent_key, child_key = key.split(".", 1)
            if parent_key not in self._internal_keys:
                raise KeyError(f"Parent key {parent_key} does not exist for deletion")
            self.__dict__[parent_key].__delitem__(child_key)
        else:
            if key in self._internal_keys:
                self._internal_keys.remove(key)
            else:
                raise KeyError(f'Key "{key}" does not exist')

    def _check_same_struct(self, other_datadict, prefix: str):
        """
        Check if the assignable portions are the same struct
        Only list, tuple, np.ndarray and torch.Tensor are checked
        """
        for k, assign in other_datadict._wrapped_items():
            new_prefix = f"{prefix}.{k}".lstrip(".")
            if k not in self.keys():
                if self._settings["strict_assign"]:
                    raise KeyError(
                        f"DataDict does not have key {new_prefix}, cannot assign. Alternatively, you can set b.settings(strict_assign=False)"
                    )
                else:
                    continue

            if isinstance(assign, DataDict):
                ours = self[k]
                assert self.is_mapping(ours), (
                    f"key {k} -> value: {ours} is not a mapping, "
                    f"cannot be assigned another mapping"
                )
                ours._check_same_struct(assign, new_prefix)
            else:
                assert self.is_sliceable(
                    self[k]
                ), f"key {k} -> value: {self[k]} is not assignable."

    def keys(self):
        return self._internal_keys

    def values(self):
        return (self[k] for k in self.keys())

    def items(self):
        return ((k, self[k]) for k in self.keys())

    def _wrapped_items(self):
        # with Immutable wrap. self.items() will unwrap the Immutables
        return ((k, self.__dict__[k]) for k in self.keys())

    def get(self, key: str, default: Optional[Any] = None):
        if key in self:  # invokes __contains__ recursively
            return self[key]
        else:
            return default

    def pop(self, key: str, default: Optional[Any] = None):
        if key in self:
            v = self[key]
            del self[key]
            return v
        else:
            return default

    def update(self, other: collections.abc.Mapping):
        if not isinstance(other, DataDict):
            other = DataDict(other)
        for k, v in other.items():
            self[k] = v

    def _preprocess_dtypes(self, dtypes, mode):
        if dtypes is None:
            dtypes = {}
        elif DataDict.is_mapping(dtypes):
            assert not any(DataDict.is_mapping(dt) for dt in dtypes.values()), (
                f"dtype spec {dtypes} cannot be nested, please use dot notation "
                f"to indicated nested keys, e.g. obs.next.sensor"
            )
            dtypes = dtypes.copy()
        else:
            dtypes = {None: dtypes}

        if mode == "numpy":
            return dtypes  # numpy can accept string as type
        elif mode == "torch":
            for k, v in dtypes.items():
                # convert string "float32" to torch.float32
                if isinstance(v, str):
                    dtypes[k] = getattr(torch, v)
            return dtypes
        else:
            raise NotImplementedError("INTERNAL", mode)

    def _match_pattern(self, key, pattern_dict):
        """
        Returns:
            matched value
        """
        for pattern, v in pattern_dict.items():
            if pattern is not None and fnmatch.fnmatch(key, pattern):
                return v

        if None in pattern_dict:  # catch-all key
            return pattern_dict[None]
        else:
            return None  # use default dtype

    def to_numpy(
        self,
        inplace: bool = True,
        dtype: Union[Dict[str, Union[str, type]], str, type, None] = None,
        copy: bool = False,
        non_blocking: bool = False,
        include_keys: Optional[List[str]] = None,
        exclude_keys: Optional[List[str]] = None,
    ):
        """
        dtypes: one of None, np.dtype, or {key_name: np.dtype}
            1. None: use default dtype inferred from the data
            2. np.dtype: use this dtype for all values
            3. a dict that maps a key to desired dtype
               nested key should be specified with dots, e.g. `obs.rgb`
               special key `None` to be a "catch-all" key
               you can also use special value `None` to automatically infer dtype
               for a given key
        """
        dtype = self._preprocess_dtypes(dtype, "numpy")

        def _convert_fn(key, value):
            if not U.match_patterns(
                key, include_keys, exclude_keys, precedence="exclude"
            ):
                # key is not matched, we don't convert and return value as-is
                return value
            return U.any_to_numpy(
                value,
                dtype=self._match_pattern(key, dtype),
                copy=copy,
                non_blocking=non_blocking,
                smart_optimize=True,
            )

        return self.map(_convert_fn, inplace=inplace, with_key=True)

    def to_tensor(
        self,
        inplace: bool = True,
        dtype: Union[Dict[str, Union[str, torch.dtype]], str, torch.dtype, None] = None,
        copy: bool = False,
        device: Union[torch.device, int, str, None] = None,
        non_blocking: bool = False,
        include_keys: Optional[List[str]] = None,
        exclude_keys: Optional[List[str]] = None,
    ):
        """
        dtypes: one of None, np.dtype, or {key_name: np.dtype}
            1. None: use default dtype inferred from the data
            2. np.dtype: use this dtype for all values
            3. a dict that maps a key to desired dtype
               nested key should be specified with dots, e.g. `obs.rgb`
               special key `None` to be a "catch-all" key
               you can also use special value `None` to automatically infer dtype
               for a given key

        device: one of None, str, or torch.device
        non_blocking: transfer to device asynchronously, see torch.Tensor.to()
        copy: force copy even when tensor dtype and device don't change, see torch.Tensor.to()
        """
        dtype = self._preprocess_dtypes(dtype, "torch")

        def _convert_fn(key, value):
            if not U.match_patterns(
                key, include_keys, exclude_keys, precedence="exclude"
            ):
                # key is not matched, we don't convert and return value as-is
                return value
            return U.any_to_torch_tensor(
                value,
                dtype=self._match_pattern(key, dtype),
                device=device,
                copy=copy,
                non_blocking=non_blocking,
                smart_optimize=True,
            )

        return self.map(_convert_fn, inplace=inplace, with_key=True)

    def _map_helper(
        self,
        fn: Callable[..., Any],
        other_datadicts,
        inplace: bool,
        prefix: str,
        with_key: bool,
    ):
        """
        Args:
            fn: (k, value) -> new_value, will only be applied to non-DataDict-type leaf nodes
        """
        ret = self if inplace else DataDict()
        for k, v in self.items():
            new_prefix = f"{prefix}.{k}".lstrip(".")  # artifact from recursion
            # unwrap to support arbitrary dict type
            other_values = [DataDict._unwrap_immutable(d[k]) for d in other_datadicts]
            if isinstance(v, DataDict):
                assert all(
                    DataDict.is_mapping(other_v) for other_v in other_values
                ), f"Map failure at key {k}: other dicts do not have the same structure"
                new_v = v._map_helper(
                    fn,
                    other_values,
                    inplace=inplace,
                    prefix=new_prefix,
                    with_key=with_key,
                )
                if not inplace:
                    # we don't assign back to `self` if inplace
                    ret[k] = new_v
            else:
                if with_key:
                    ret[k] = fn(new_prefix, v, *other_values)
                else:
                    ret[k] = fn(v, *other_values)
        return ret

    def map(
        self,
        fn: Callable[..., Any],
        *other_datadicts,
        inplace: bool = False,
        with_key: bool = False,
    ):
        return self._map_helper(
            fn, other_datadicts, inplace, prefix="", with_key=with_key
        )

    @staticmethod
    def multi_map(fn: Callable[..., Any], *datadicts, with_key: bool = False):
        """
        Args:        
            fn(*values) -> new_value
        """
        assert len(datadicts) >= 1, "must have at least one DataDict"
        d0 = datadicts[0]
        if not isinstance(d0, DataDict):
            d0 = DataDict(d0)
        return d0.map(fn, *datadicts[1:], inplace=False, with_key=with_key)

    def _traverse_helper(
        self, fn: Callable[..., None], other_datadicts, prefix: str, with_key: bool
    ):
        """
        Args:
            fn: (k, value) -> new_value, will only be applied to non-DataDict-type leaf nodes
        """
        for k, v in self.items():
            new_prefix = f"{prefix}.{k}".lstrip(".")  # artifact from recursion
            # unwrap to support arbitrary dict type
            other_values = [DataDict._unwrap_immutable(d[k]) for d in other_datadicts]
            if isinstance(v, DataDict):
                assert all(
                    DataDict.is_mapping(other_v) for other_v in other_values
                ), f"Traversal failure at key {k}: other dicts do not have the same structure"
                v._traverse_helper(
                    fn, other_values, prefix=new_prefix, with_key=with_key
                )
            else:
                if with_key:
                    fn(new_prefix, v, *other_values)
                else:
                    fn(v, *other_values)

    def traverse(
        self, fn: Callable[..., None], *other_datadicts, with_key: bool = False
    ):
        return self._traverse_helper(fn, other_datadicts, prefix="", with_key=with_key)

    @staticmethod
    def multi_traverse(fn: Callable[..., None], *datadicts, with_key: bool = False):
        assert len(datadicts) >= 1, "must have at least one DataDict"
        d0 = datadicts[0]
        if not isinstance(d0, DataDict):
            d0 = DataDict(d0)
        d0.traverse(fn, *datadicts[1:], with_key=with_key)

    def __contains__(self, key: str):
        if "." in key:
            parent_key, child_key = key.split(".", 1)
            return self.__dict__[parent_key].__contains__(child_key)
        else:
            return key in self._internal_keys

    def __iter__(self):
        return iter(self.keys())

    def __len__(self) -> int:
        return len(self.keys())

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        INDENT = 4
        s = cls_name + " {\n"
        flag = False
        for k in self._internal_keys:
            rpl = "\n" + " " * INDENT
            obj = pprint.pformat(self.__dict__[k]).replace("\n", rpl)
            s += " " * INDENT + f"{k}: {obj},\n"
            flag = True
        if flag:
            s += "}"
        else:
            s = cls_name + "{}"
        return s
