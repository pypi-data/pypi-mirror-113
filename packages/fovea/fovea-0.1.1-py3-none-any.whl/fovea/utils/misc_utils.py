import os
import numpy as np
import fnmatch
import collections.abc
from typing import Optional, Dict, Any, List, Union


def get_human_readable_count(number: int, precision: int = 2):
    assert number >= 0
    labels = [" ", "K", "M", "B", "T"]
    num_digits = int(np.floor(np.log10(number)) + 1 if number > 0 else 1)
    num_groups = int(np.ceil(num_digits / 3))
    num_groups = min(num_groups, len(labels))  # don't abbreviate beyond trillions
    shift = -3 * (num_groups - 1)
    number = number * (10 ** shift)
    index = num_groups - 1
    rem = number - int(number)
    if precision > 0 and rem > 0.01:
        fmt = f"{{:.{precision}f}}"
        rem_str = fmt.format(rem).lstrip("0")
    else:
        rem_str = ""
    return f"{int(number):,d}{rem_str} {labels[index]}"


def set_os_envs(envs: Optional[Dict[str, Any]] = None):
    """
    Special value __delete__ indicates that the ENV_VAR should be removed
    """
    if envs is None:
        envs = {}
    # check for special key __delete__
    for k, v in envs.items():
        if v == "__delete__":
            os.environ.pop(k, None)
    os.environ.update({k: str(v) for k, v in envs.items() if v != "__delete__"})


def _match_patterns_helper(element, patterns):
    for p in patterns:
        if fnmatch.fnmatch(element, p):
            return True
    return False


def match_patterns(
    element,
    include: Union[str, List[str], None] = None,
    exclude: Union[str, List[str], None] = None,
    *,
    precedence: str = "exclude",
):
    """
    Args:
        include: None to disable `include` filter and delegate to exclude
        precedence: "include" or "exclude"
    """
    assert precedence in ["include", "exclude"]
    if exclude is None:
        exclude = []
    if isinstance(exclude, str):
        exclude = [exclude]
    if isinstance(include, str):
        include = [include]
    if include is None:
        # exclude is the sole veto vote
        return not _match_patterns_helper(element, exclude)

    if precedence == "include":
        return _match_patterns_helper(element, include)
    else:
        if _match_patterns_helper(element, exclude):
            return False
        else:
            return _match_patterns_helper(element, include)
