import os
import socket
import torch
import torch.distributed as _dist
from typing import List

try:
    import apex.parallel
    _HAS_NVIDIA_APEX = True
except ImportError:
    _HAS_NVIDIA_APEX = False


def has_nvidia_apex():
    return _HAS_NVIDIA_APEX


def has_pytorch_syncbn():
    """
    PyTorch >= 1.2 supports SyncBN
    PyTorch 1.1 supports too, but there is a process_group bug:

    It didn't pass in process_group to children module recursively
    https://github.com/pytorch/pytorch/pull/19240
    """
    from pkg_resources import parse_version
    return parse_version(torch.__version__) >= parse_version('1.2.0')


def _get_group(group):
    if group is None:
        return _dist.group.WORLD
    else:
        return group


get_rank = _dist.get_rank
get_world_size = _dist.get_world_size


def is_master(group=None):
    return _dist.get_rank(_get_group(group)) == 0


def get_backend(group=None):
    return _dist.get_backend(group)


def current_device():
    return torch.cuda.current_device()


def optimize_cudnn():
    import torch.backends.cudnn as _cudnn

    _cudnn.benchmark = True
    _cudnn.deterministic = False


def get_reduce_op(op):
    OPS = {
        "sum": _dist.ReduceOp.SUM,
        "mean": _dist.ReduceOp.SUM,  # no buildin for mean, we handle it ourselves
        "product": _dist.ReduceOp.PRODUCT,
        "max": _dist.ReduceOp.MAX,
        "min": _dist.ReduceOp.MIN,
    }
    op = op.lower()
    assert op in OPS, "invalid op: " + op
    return OPS[op]


def random_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(("", 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port


def get_cuda_visible_devices() -> List[int]:
    """
    parse CUDA_VISIBLE_DEVICES
    """
    if 'CUDA_VISIBLE_DEVICES' not in os.environ:
        return []
    devices = os.environ['CUDA_VISIBLE_DEVICES']
    return [int(g) for g in devices.strip(' ,').split(',')]