import math
import torch.utils.data
import torch.distributed as dist


__all__ = [
    "EpochRandomSampler",
    "DistributedRandomSampler",
    "DistributedSequentialSampler",
]


class EpochRandomSampler(torch.utils.data.Sampler):
    """
    Single process sampler. Deterministic sampling based on epoch number.
    """

    def __init__(self, dataset, start_epoch, base_seed=0):
        super().__init__(dataset)
        self.dataset = dataset
        self.epoch = start_epoch
        self.base_seed = base_seed

    @property
    def seed(self):
        return self.base_seed + self.epoch

    def __iter__(self):
        # deterministically shuffle based on epoch
        g = torch.Generator()
        g.manual_seed(self.seed)
        indices = torch.randperm(len(self.dataset), generator=g).tolist()
        self.epoch += 1
        return iter(indices)

    def __len__(self):
        return len(self.dataset)


class DistributedRandomSampler(torch.utils.data.Sampler):
    """
    Similar to torch.utils.data.distributed.DistributedSampler, but can automatically
    increment epoch.
    """

    def __init__(self, dataset, start_epoch, base_seed=0, num_replicas=None, rank=None):
        """
        Args:
            base_seed: actual seed used will be `epoch + seed`
        """
        super().__init__(dataset)
        if num_replicas is None:
            if not dist.is_available():
                raise RuntimeError("Requires distributed package to be available")
            num_replicas = dist.get_world_size()
        if rank is None:
            if not dist.is_available():
                raise RuntimeError("Requires distributed package to be available")
            rank = dist.get_rank()
        self.dataset = dataset
        self.num_replicas = num_replicas
        self.rank = rank
        self.epoch = start_epoch
        self.base_seed = base_seed
        self.num_samples = int(math.ceil(len(self.dataset) * 1.0 / self.num_replicas))
        self.total_size = self.num_samples * self.num_replicas

    @property
    def seed(self):
        return self.base_seed + self.epoch

    def __iter__(self):
        # deterministically shuffle based on epoch
        g = torch.Generator()
        g.manual_seed(self.seed)
        indices = torch.randperm(len(self.dataset), generator=g).tolist()
        self.epoch += 1

        # add extra samples to make it evenly divisible
        indices += indices[: (self.total_size - len(indices))]
        assert len(indices) == self.total_size

        # subsample
        indices = indices[self.rank : self.total_size : self.num_replicas]
        assert len(indices) == self.num_samples

        return iter(indices)

    def __len__(self):
        return self.num_samples


class DistributedSequentialSampler(torch.utils.data.Sampler):
    """
    Sequential sampling for distributed val mode
    """

    def __init__(self, dataset, num_replicas=None, rank=None):
        super().__init__(dataset)
        if num_replicas is None:
            if not dist.is_available():
                raise RuntimeError("Requires distributed package to be available")
            num_replicas = dist.get_world_size()
        if rank is None:
            if not dist.is_available():
                raise RuntimeError("Requires distributed package to be available")
            rank = dist.get_rank()
        self.dataset = dataset
        self.num_replicas = num_replicas
        self.rank = rank
        self.num_samples = int(math.ceil(len(self.dataset) * 1.0 / self.num_replicas))
        self.total_size = self.num_samples * self.num_replicas

    def __iter__(self):
        indices = list(range(len(self.dataset)))
        # add extra samples to make it evenly divisible
        indices += indices[: (self.total_size - len(indices))]
        assert len(indices) == self.total_size

        # subsample
        indices = indices[self.rank : self.total_size : self.num_replicas]
        assert len(indices) == self.num_samples

        return iter(indices)

    def __len__(self):
        return self.num_samples
