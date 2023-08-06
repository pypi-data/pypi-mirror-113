import torch
import numpy as np


def to_np(t):
    if t is None:
        return None
    elif t.nelement() == 0:
        return np.array([])
    else:
        return t.cpu().detach().numpy()


def np_unsqueeze(x, dim=0):
    """
    Simulate torch.unsqueeze
    """
    return np.expand_dims(x, axis=dim)

