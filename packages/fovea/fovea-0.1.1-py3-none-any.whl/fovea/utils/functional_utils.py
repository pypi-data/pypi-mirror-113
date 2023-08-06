"""
Inspect, meta, etc.
"""
import inspect


def func_parameters(func):
    return inspect.signature(func).parameters


def func_has_arg(func, arg_name):
    return arg_name in func_parameters(func)
