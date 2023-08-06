import os
import numpy as np
import torch
import random
import time
import torch.nn as nn
from copy import deepcopy
from typing import Optional, Union


def weight_init(m):
    """Custom weight init for Conv2D and Linear layers."""
    if isinstance(m, nn.Linear):
        nn.init.orthogonal_(m.weight.data)
        if hasattr(m.bias, "data"):
            m.bias.data.fill_(0.0)
    elif isinstance(m, nn.Conv2d) or isinstance(m, nn.ConvTranspose2d):
        gain = nn.init.calculate_gain("relu")
        nn.init.orthogonal_(m.weight.data, gain)
        if hasattr(m.bias, "data"):
            m.bias.data.fill_(0.0)


def set_seed_everywhere(
    seed: Optional[Union[int, str]], deterministic=False
) -> Optional[int]:
    """
    seed:
        None, "time", "sys": use scrambled system time
        int < 0, "noop", "skip": do nothing
        int >= 0: set seed
    """
    if seed is None or seed in ["time", "sys"]:
        # https://stackoverflow.com/questions/27276135/python-random-system-time-seed
        t = int(time.time() * 100000)
        seed = (
            ((t & 0xFF000000) >> 24)
            + ((t & 0x00FF0000) >> 8)
            + ((t & 0x0000FF00) << 8)
            + ((t & 0x000000FF) << 24)
        )
    if seed < 0 or seed in ["noop", "skip"]:
        return None
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    if deterministic:
        import torch.backends.cudnn as cudnn

        cudnn.deterministic = True
        cudnn.benchmark = False
    return seed


class eval_mode(object):
    def __init__(self, *models):
        self.models = models

    def __enter__(self):
        self.prev_states = []
        for model in self.models:
            self.prev_states.append(model.training)
            model.train(False)

    def __exit__(self, *args):
        for model, state in zip(self.models, self.prev_states):
            model.train(state)
        return False


# ========== module operations =========
def set_requires_grad(model, requires_grad):
    for param in model.parameters():
        param.requires_grad = requires_grad


def freeze_params(model):
    set_requires_grad(model, False)


def unfreeze_params(model):
    set_requires_grad(model, True)


def clip_grad_value(model, max_value):
    with torch.no_grad():
        nn.utils.clip_grad_value_(model.parameters(), max_value)


def clip_grad_norm(model, max_norm, norm_type=2):
    """
    Returns:
        Total norm of the parameters (viewed as a single vector).
    """
    with torch.no_grad():
        return nn.utils.clip_grad_norm_(
            model.parameters(), max_norm=max_norm, norm_type=norm_type
        )


def count_parameters(model):
    return sum(x.numel() for x in model.parameters())


def get_model_device(model):
    """
    Returns:
        first model parameter's device
    """
    return next(model.parameters()).device


def clone_model(model):
    # with torch.no_grad():
    new_model = deepcopy(model).to(get_model_device(model))
    # new_model.load_state_dict(model.state_dict())
    return new_model


def update_soft_params(net, target_net, tau):
    for param, target_param in zip(net.parameters(), target_net.parameters()):
        target_param.data.copy_(tau * param.data + (1 - tau) * target_param.data)


def tie_weights(src, trg):
    # TODO deprecate this
    assert type(src) == type(trg)
    trg.weight = src.weight
    trg.bias = src.bias


def torch_normalize(tensor: torch.Tensor, mean, std, inplace=False):
    """
    Adapted from https://pytorch.org/docs/stable/_modules/torchvision/transforms/functional.html#normalize

    Normalize a tensor image with mean and standard deviation.

    .. note::
        This transform acts out of place by default, i.e., it does not mutates the input tensor.

    See :class:`~torchvision.transforms.Normalize` for more details.

    Args:
        tensor (Tensor): Tensor image of size (C, H, W) to be normalized.
        mean (sequence): Sequence of means for each channel.
        std (sequence): Sequence of standard deviations for each channel.
        inplace(bool,optional): Bool to make this operation inplace.

    Returns:
        Tensor: Normalized Tensor image.
    """
    if not torch.is_tensor(tensor):
        raise TypeError("tensor should be a torch tensor. Got {}.".format(type(tensor)))

    if not inplace:
        tensor = tensor.clone()

    dtype = tensor.dtype
    mean = torch.as_tensor(mean, dtype=dtype, device=tensor.device)
    std = torch.as_tensor(std, dtype=dtype, device=tensor.device)
    if (std == 0).any():
        raise ValueError(
            f"std evaluated to zero after conversion to {dtype}, leading to division by zero."
        )
    if mean.ndim == 1:
        mean = mean[:, None, None]
    if std.ndim == 1:
        std = std[:, None, None]
    tensor.sub_(mean).div_(std)
    return tensor
