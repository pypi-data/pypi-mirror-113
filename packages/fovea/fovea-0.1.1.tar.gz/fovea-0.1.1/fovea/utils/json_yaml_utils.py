"""
JSON, YAML, and python config file utilities
"""
import json
import yaml
import os.path as path
from io import StringIO


__all__ = [
    "json_load",
    "json_loads",
    "yaml_load",
    "yaml_loads",
    "json_dump",
    "json_dumps",
    "yaml_dump",
    "yaml_dumps",
    "json_or_yaml_load",
    "json_or_yaml_dump",
]


def json_load(file_path, **kwargs):
    file_path = path.expanduser(file_path)
    with open(file_path, "r") as fp:
        return json.load(fp, **kwargs)


def json_loads(string, **kwargs):
    return json.loads(string, **kwargs)


def json_dump(data, file_path, **kwargs):
    file_path = path.expanduser(file_path)
    with open(file_path, "w") as fp:
        indent = kwargs.pop("indent", 4)
        json.dump(data, fp, indent=indent, **kwargs)


def json_dumps(data, **kwargs):
    "Returns: string"
    return json.dumps(data, **kwargs)


def yaml_load(file_path, *, loader=yaml.safe_load, **kwargs):
    file_path = path.expanduser(file_path)
    with open(file_path, "r") as fp:
        return loader(fp, **kwargs)


def yaml_loads(string, *, loader=yaml.safe_load, **kwargs):
    return loader(string, **kwargs)


def yaml_dump(data, file_path, *, dumper=yaml.safe_dump, **kwargs):
    file_path = path.expanduser(file_path)
    indent = kwargs.pop("indent", 2)
    default_flow_style = kwargs.pop("default_flow_style", False)
    with open(file_path, "w") as fp:
        dumper(
            data,
            stream=fp,
            indent=indent,
            default_flow_style=default_flow_style,
            **kwargs
        )


def yaml_dumps(data, *, dumper=yaml.safe_dump, **kwargs):
    "Returns: string"
    stream = StringIO()
    indent = kwargs.pop("indent", 2)
    default_flow_style = kwargs.pop("default_flow_style", False)
    dumper(data, stream, indent=indent, default_flow_style=default_flow_style, **kwargs)
    return stream.getvalue()


# ==================== auto-recognize extension ====================
def json_or_yaml_load(file_path, **loader_kwargs):
    """
    Args:
        file_path: JSON or YAML loader depends on the file extension

    Raises:
        IOError: if extension is not ".json", ".yml", or ".yaml"
    """
    if file_path.endswith(".json"):
        return json_load(file_path, **loader_kwargs)
    elif file_path.endswith(".yml") or file_path.endswith(".yaml"):
        return yaml_load(file_path, **loader_kwargs)
    else:
        raise IOError(
            'unknown file extension: "{}", loader supports only ".json", ".yml", ".yaml"'.format(
                file_path
            )
        )


def json_or_yaml_dump(data, file_path, **dumper_kwargs):
    """
    Args:
        file_path: JSON or YAML loader depends on the file extension

    Raises:
        IOError: if extension is not ".json", ".yml", or ".yaml"
    """
    if file_path.endswith(".json"):
        return json_dump(data, file_path, **dumper_kwargs)
    elif file_path.endswith(".yml") or file_path.endswith(".yaml"):
        return yaml_dump(data, file_path, **dumper_kwargs)
    else:
        raise IOError(
            'unknown file extension: "{}", dumper supports only ".json", ".yml", ".yaml"'.format(
                file_path
            )
        )
