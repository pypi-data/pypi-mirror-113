import torch
import functools
import collections.abc
from .core import ExtendedModule, LightningModule


class _Cache:
    """
    Hold training cache
    """
    pass


class MultiOptimizerModule(ExtendedModule):
    """
    Subclass should still have only `hparams` in the arg, and call
    super().__init__(hparams, ...)

    configure_optimizer() method should return a dict instead of a list of optimizers:
    order should be respected
    { 'actor': SGD(), 'critic1': Adam(), 'critic2': Adam() }
    """

    def __new__(cls, *args, **kwargs):
        """
        Class-level patch to avoid multiprocessing pickle error:
            _pickle.PicklingError: Can't pickle <function .. at ..>: it's not
            the same object as __main__.<obj>
        """
        obj = super().__new__(cls)
        cls._patch_configure_optimizer()
        return obj

    def __init__(self, hparams, group_spec):
        """
        group_spec:
        {
            'actor': {
                'interval': 1,
                'training_step_method': self.actor_training_step,
                'optimizer_step_method': <optional>
            },
            'critic1': {
                'interval': 4,
                'training_step_method': self.critic1_training_step,
            },
            'critic2': {
                'interval': 8,
                'training_step_method': self.critic2_training_step,
            }
        }

        NOTE:
          - the optimizer index order will be the same as timescale_spec dict key order
          - training_step_method signature: f(batch, batch_idx) -> output dict
          - optimizer_step_method signature: f(epoch, batch_idx, optimizer, second_order_closure) -> None

        """
        super().__init__(hparams)
        self._group_ordering = []
        assert (
            len(group_spec) >= 2
        ), "must have at least two optimizers to use MultiOptimizerModule"
        for name, conf in group_spec.items():
            assert "interval" in conf and isinstance(conf["interval"], int)
            assert "training_step_method" in conf and callable(
                conf["training_step_method"]
            )
            if "optimizer_step_method" in conf:
                assert callable(conf["optimizer_step_method"])
            else:
                conf["optimizer_step_method"] = None
            self._group_ordering.append(name)
        self.group_spec = group_spec
        self.training_cache = _Cache()
        # dummy loss for skipping training steps
        self._dummy_loss = torch.tensor(0.0, requires_grad=True)

    @property
    def dummy_loss(self):
        return self._dummy_loss.to(self.device)

    def training_step(self, batch, batch_idx, optimizer_idx):
        assert optimizer_idx < len(self._group_ordering), "INTERNAL"
        name = self._group_ordering[optimizer_idx]
        if optimizer_idx == 0:  # first iter over optimizer
            self.training_cache = _Cache()  # reset cache
            self.common_training_step(batch, batch_idx)
        if self.is_training_step_triggered(
            name=name, batch_idx=batch_idx, optimizer_idx=optimizer_idx
        ):
            # self.log_debug('TRIGGER_train_step', name, batch_idx)
            _training_step = self.group_spec[name]["training_step_method"]
            return _training_step(batch, batch_idx)
        else:
            # return a dummy value required by LightningModule
            return {"loss": self._dummy_loss}

    def optimizer_step(
        self,
        epoch: int,
        batch_idx: int,
        optimizer,
        optimizer_idx: int,
        second_order_closure=None,
    ) -> None:
        assert optimizer_idx < len(self._group_ordering), "INTERNAL"
        name = self._group_ordering[optimizer_idx]
        if self.is_training_step_triggered(
            name=name, batch_idx=batch_idx, optimizer_idx=optimizer_idx
        ):
            _optimizer_step = self.group_spec[name]["optimizer_step_method"]
            # self.log_debug('TRIGGER_optimizer_step', name, batch_idx)
            if _optimizer_step is None:
                # default implementation: does not use optimizer_idx in the code
                LightningModule.optimizer_step(
                    self,
                    epoch=epoch,
                    batch_idx=batch_idx,
                    optimizer=optimizer,
                    optimizer_idx=optimizer_idx,
                    second_order_closure=second_order_closure,
                )
            else:
                _optimizer_step(
                    epoch=epoch,
                    batch_idx=batch_idx,
                    optimizer=optimizer,
                    second_order_closure=second_order_closure,
                )

    def is_training_step_triggered(
        self, *, name: str, batch_idx: int, optimizer_idx: int
    ):
        """
        User can override this method to trigger at arbitrary times

        Args:
            name: optimizer group name
        """
        return batch_idx % self.group_spec[name]["interval"] == 0

    def common_training_step(self, batch, batch_idx):
        """
        User can override this method, will be called before optimizer_idx == 0
        Will be called once and only once.
        Write any intermediate saving to self.training_cache
        """
        return None

    @classmethod
    def _patch_configure_optimizer(cls):
        pl_method = cls.configure_optimizers

        @functools.wraps(pl_method)
        def _wrapped(self: MultiOptimizerModule):
            ret = pl_method(self)
            if isinstance(ret, tuple) and len(ret) == 2:
                optimizer_cfg, scheduler_cfg = ret
            else:
                optimizer_cfg, scheduler_cfg = ret, None
            if not isinstance(optimizer_cfg, collections.abc.Mapping):
                raise RuntimeError(
                    f"MultiOptimizerModule: configure_optimizer must return a dictionary of optimizers with the name you specified in `group_spec` at __init__"
                )
            if set(optimizer_cfg.keys()) != set(self.group_spec.keys()):
                raise KeyError(
                    f"Optimizer names {optimizer_cfg.keys()} do not match with `group_spec` names {self.group_spec.keys()}"
                )

            # we return Lightning-compatible list of optimziers in the order of timescale_spec
            optimizer_cfg = [optimizer_cfg[key] for key in self.group_spec]

            if scheduler_cfg is None:
                return optimizer_cfg
            else:
                return optimizer_cfg, scheduler_cfg

        # monkey patch
        cls.configure_optimizers = _wrapped
