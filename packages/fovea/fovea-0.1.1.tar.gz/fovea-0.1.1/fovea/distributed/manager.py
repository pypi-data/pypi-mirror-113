"""
https://pytorch.org/docs/stable/distributed.html
https://pytorch.org/docs/stable/data.html#torch.utils.data.distributed.DistributedSampler
https://pytorch.org/docs/stable/distributed.html#launch-utility

Complete working example:
https://github.com/pytorch/examples/blob/master/imagenet/main.py

Wrapper around nn.DataParallel and nn.parallel.DistributedDataParallel
"""
import os
import copy
import random
import numpy as np
import torch
import torch.nn as nn
import torch.distributed as dist
import torch.utils.data
import omlet.utils as U
from omlet.data.loaders import *
from .utils import *


__all__ = [
    "WorkerManager",
    "get_local_rank",
    "is_master",
    "get_global_rank",
    "get_world_size",
]

# https://discuss.pytorch.org/t/issue-with-multiprocessing-semaphore-tracking/22943/4
os.environ["PYTHONWARNINGS"] = "ignore:semaphore_tracker:UserWarning"


# FIXME: merge these with pytorch get_rank, get_world_size


def get_local_rank():
    """
    We can obtain process local_rank without using WorkerManager
    """
    return int(os.environ.get("TORCHX_LOCAL_RANK", 0))


def is_master(local=True):
    if local:
        return get_local_rank() == 0
    else:
        return get_global_rank() == 0


def get_global_rank():
    return int(os.environ.get("TORCHX_GLOBAL_RANK", 0))


def get_world_size():
    return int(os.environ.get("TORCHX_WORLD_SIZE", 0))


class _AutoDeviceDataLoader(torch.utils.data.DataLoader):
    def _set_device(self, mode, device):
        self.__mode = mode
        self.__device = device

    def __iter__(self):
        for batch_data in super().__iter__():
            if not isinstance(batch_data, (tuple, list)) or len(batch_data) != 2:
                # yield without change if not in the format of (input, target) pair
                yield batch_data
            else:
                # For DataParallel, we put `input` on CPU because we don't
                # want to send the entire unsharded input to the first GPU.
                input, target = batch_data
                if self.__mode != "dp":
                    input = input.cuda(self.__device, non_blocking=True)
                target = target.cuda(self.__device, non_blocking=True)
                yield input, target


class WorkerManager:
    disable_warning = False
    DEFAULT_GROUP = dist.group.WORLD

    def __init__(
        self,
        local_rank,
        global_rank,
        world_size,
        gpu_indices,
        mode,
        backend,
        group,
        group_ids,
        print_options,
    ):
        self.local_rank = local_rank
        self.global_rank = global_rank
        self.world_size = world_size
        assert self.local_rank < len(gpu_indices), "internal error"
        self.gpu_indices = gpu_indices
        self.mode = mode
        self.backend = backend
        self.group = group  # process group
        self.group_ids = group_ids
        self.print_options = print_options
        self.print_options["process_rank"] = self.local_rank
        if "ddp" not in self.mode:
            self.print_options["broadcast"] = False

    @property
    def gpu_idx(self):
        mode = self.mode
        if mode in ["ddp", "ddp_apex", "dp"]:
            return self.gpu_indices[self.local_rank]
        elif mode == "single":
            assert len(self.gpu_indices) == 1
            return self.gpu_indices[0]
        else:
            raise NotImplementedError

    def device(self):
        return torch.device(self.gpu_idx)

    def device_context(self):
        """
        Context manager
        """
        return torch.cuda.device(self.device())

    def is_default_group(self):
        return self.group == self.DEFAULT_GROUP

    def is_ddp(self):
        return self.mode in ["ddp", "ddp_apex"]

    def is_single(self):
        return self.mode == "single"

    def is_master(self, local=True):
        if local:
            return self.local_rank == 0
        else:
            return self.global_rank == 0

    def is_worker(self):
        return not self.is_master()

    @property
    def num_gpus(self):
        return len(self.gpu_indices)

    def get_local_batch_size(self, global_batch_size):
        divisor = self.num_gpus if self.is_ddp() else 1
        return int(global_batch_size / divisor)

    def data_parallel(self, model, sync_bn=False, sync_bn_group=None, **kwargs):
        """
        Args:
            sync_bn_group: if None, defaults to syncBN over the entire `world`
        """
        mode = self.mode
        if sync_bn:
            if mode == "ddp":
                assert (
                    has_pytorch_syncbn()
                ), "must use pytorch version >= 1.2 for SyncBN. Otherwise you can use Nvidia apex syncBN."
            else:
                assert (
                    mode == "ddp_apex"
                ), "SyncBN is only supported with Nvidia Apex or pytorch version >= 1.2"
            if sync_bn_group is None:
                sync_bn_group = self.DEFAULT_GROUP

        if mode == "ddp":
            device = self.device()
            model.cuda(device)
            if sync_bn:
                model = nn.SyncBatchNorm.convert_sync_batchnorm(model, sync_bn_group)
            return nn.parallel.DistributedDataParallel(
                model, device_ids=[device], output_device=device, **kwargs
            )
        elif mode == "ddp_apex":
            assert has_nvidia_apex()
            from apex.parallel import (
                DistributedDataParallel as ApexDistributedDataParallel,
            )
            from apex.parallel import convert_syncbn_model as apex_convert_syncbn_model

            if sync_bn:
                model = apex_convert_syncbn_model(model, process_group=sync_bn_group)
            model.cuda(self.device())
            kwargs = copy.deepcopy(kwargs)
            # defaults to True unless explicitly specified
            delay_allreduce = kwargs.pop("delay_allreduce", True)
            return ApexDistributedDataParallel(
                model, delay_allreduce=delay_allreduce, **kwargs
            )
        elif mode == "dp":
            return nn.DataParallel(model, device_ids=self.gpu_indices, **kwargs).cuda()
        elif mode == "single":
            return model.cuda(self.device())
        else:
            raise NotImplementedError

    def unwrap(self, model):
        """
        Retrieve the model wrapped in DataParallel
        """
        if self.mode == "single":
            return model
        else:
            assert hasattr(
                model, "module"
            ), "internal error: dp or ddp-wrapped model has no `.module` attribute"
            return model.module

    def get_data_loader(
        self,
        dataset,
        global_batch_size,
        num_workers,
        stage,
        epoch=None,
        keep_on_cpu=False,
        **loader_kwargs
    ):
        assert stage in ["train", "val", "test"]
        mode = self.mode
        batch_size = self.get_local_batch_size(global_batch_size)
        divisor = self.num_gpus if self.is_ddp() else 1
        num_workers = int(num_workers / divisor)
        LoaderCls = (
            torch.utils.data.DataLoader if keep_on_cpu else _AutoDeviceDataLoader
        )
        if self.is_ddp():
            if stage == "train":
                assert isinstance(
                    epoch, int
                ), "`epoch` must be specified in order to use DistributedSampler in training, because it is used as the internal random seed."
                sampler = DistributedRandomSampler(dataset, start_epoch=epoch)
            else:
                sampler = DistributedSequentialSampler(dataset)
            # sampler = torch.utils.data.distributed.DistributedSampler(dataset)
            self._warning(
                """
                DistributedSampler makes the dataloader 1/num_gpu shorter. 
                Loss and accuracy values will be calculated from only 1/num_gpu data if you don't call manager.all_reduce() or .master_reduce() manually. 
                """
            )
        else:
            sampler = None
        if stage == "train":
            shuffle = sampler is None
        else:
            shuffle = False

        loader = LoaderCls(
            dataset,
            batch_size=batch_size,
            shuffle=shuffle,
            num_workers=num_workers,
            pin_memory=True,
            sampler=sampler,
            **loader_kwargs
        )
        if isinstance(loader, _AutoDeviceDataLoader):
            loader._set_device(mode, self.device())
        return loader

    def set_seed(self, seed=111, same_worker_seed=True, deterministic=False):
        if not same_worker_seed and seed is not None:
            seed = seed + self.local_rank
        U.set_seed_everywhere(seed, deterministic=deterministic)

    def _get_reduce_op(self, op):
        # TODO fix
        OPS = {
            "sum": dist.ReduceOp.SUM,
            "mean": dist.ReduceOp.SUM,  # no buildin for mean, we handle it ourselves
            "product": dist.ReduceOp.PRODUCT,
            "max": dist.ReduceOp.MAX,
            "min": dist.ReduceOp.MIN,
        }
        op = op.lower()
        assert op in OPS, "invalid op: " + op
        return OPS[op]

    def all_reduce_(self, tensor, op="sum", group=None):
        """
        Warnings:
            input tensor will be mutated
        """
        if group is None:
            group = self.DEFAULT_GROUP
        if self.is_ddp():
            assert torch.is_tensor(tensor)
            dist.all_reduce(tensor, op=self._get_reduce_op(op), group=group)
            if op.lower() == "mean":
                tensor.div_(1.0 * dist.get_world_size())

    def all_reduce(self, tensor, op="sum", group=None):
        """
        Immutable version of all_reduce_
        Leave input tensor unchanged, return a copied reduced version
        """
        if group is None:
            group = self.DEFAULT_GROUP
        if self.is_ddp():
            assert torch.is_tensor(tensor)
            new_tensor = tensor.clone().detach()
            dist.all_reduce(new_tensor, op=self._get_reduce_op(op), group=group)
            if op.lower() == "mean":
                new_tensor.div_(1.0 * dist.get_world_size())
            return new_tensor
        else:
            return tensor

    def master_reduce_(self, tensor, op="sum", group=None):
        """
        Reduced result is only available on master proc.
        Other worker procs will leave input tensor unchanged
        Warnings:
            input tensor will be mutated on the master proc
        """
        if group is None:
            group = self.DEFAULT_GROUP
        if self.is_ddp():
            assert torch.is_tensor(tensor)
            dist.reduce(tensor, dst=0, op=self._get_reduce_op(op), group=group)
            if op.lower() == "mean" and self.is_master():
                tensor.div_(1.0 * dist.get_world_size())

    def master_reduce(self, tensor, op="sum", group=None):
        """
        Immutable version of master_reduce_
        Leave input tensor unchanged, return a copied reduced version
        """
        if group is None:
            group = self.DEFAULT_GROUP
        if self.is_ddp():
            assert torch.is_tensor(tensor)
            new_tensor = tensor.clone().detach()
            dist.reduce(new_tensor, dst=0, op=self._get_reduce_op(op), group=group)
            if op.lower() == "mean" and self.is_master():
                new_tensor.div_(1.0 * dist.get_world_size())
            return new_tensor
        else:
            return tensor

    def sync_barrier(self):
        if self.is_ddp():
            dist.barrier()

    def reduce_scalar(
        self, scalar, op="sum", *, broadcast=True, storage=None, group=None
    ):
        """
        Args:
            scalar: single python float
            broadcast: True to use all_reduce, else master_reduce
            storage: if you call this method repeatedly, consider allocating
                a persistent CUDA tensor in advance to provide temporary storage
                if None, allocates new CUDA memory every time
        Returns:
            python float
        """
        scalar = float(scalar)
        if not self.is_ddp():
            return scalar
        if storage is None:
            s = torch.tensor([scalar], dtype=torch.float32)
            if self.backend == "nccl":
                s = s.cuda(self.device())
        else:
            assert torch.is_tensor(storage)
            assert storage.numel() > 0, "storage must have at least 1 element"
            if self.backend == "nccl":
                assert storage.is_cuda
            storage[0] = scalar
            s = storage
        reduce_ = self.all_reduce_ if broadcast else self.master_reduce_
        reduce_(s, op=op, group=group)
        return float(s[0])

    def reduce_scalars(
        self, scalars, op="sum", *, broadcast=True, storage=None, group=None
    ):
        """
        Args:
            scalars: list, tuple or dict of python floats
            broadcast: True to use all_reduce, else master_reduce
            storage: if you call this method repeatedly, consider allocating
                a persistent CUDA tensor in advance to provide temporary storage
                if None, allocates new CUDA memory every time
        Returns:
            list, tuple or dict of reduced floats
        """
        if not isinstance(scalars, (tuple, list, dict)):
            # singleton falls back to reduce_scalar()
            return self.reduce_scalar(
                scalars, op=op, broadcast=broadcast, storage=storage
            )
        if not self.is_ddp():
            return scalars
        idx_map = None
        if isinstance(scalars, dict):
            values = []
            idx_map = {}
            for i, (k, v) in enumerate(scalars.items()):
                idx_map[k] = i
                values.append(float(v))
        else:
            values = [float(v) for v in scalars]
        numel = len(values)

        values = torch.tensor(values, dtype=torch.float32)
        if storage is None:
            if self.backend == "nccl":
                values = values.cuda(self.device())
        else:
            assert torch.is_tensor(storage)
            assert storage.numel() >= numel, "storage not enough"
            if self.backend == "nccl":
                assert storage.is_cuda
            storage[:numel] = values
            values = storage
        reduce_ = self.all_reduce_ if broadcast else self.master_reduce_
        reduce_(values, op=op, group=group)

        if isinstance(scalars, dict):
            return {k: float(values[idx_map[k]]) for k in idx_map}
        else:
            return type(scalars)(float(v) for v in values[:numel])

    def print(self, *objs, broadcast=None, **print_kwargs):
        """
        Args:
            broadcast: if None, inherits the broadcast print option from DistLauncher
        """
        opts = self.print_options.copy()
        if broadcast is not None:
            opts["broadcast"] = broadcast

        U.print_multiprocess(*objs, **opts, **print_kwargs)

    def printfmt(self, fmt_str, *fmt_args, broadcast=None, **fmt_kwargs):
        opts = self.print_options.copy()
        if broadcast is not None:
            opts["broadcast"] = broadcast

        U.printfmt_multiprocess(fmt_str, *fmt_args, **opts, **fmt_kwargs)
