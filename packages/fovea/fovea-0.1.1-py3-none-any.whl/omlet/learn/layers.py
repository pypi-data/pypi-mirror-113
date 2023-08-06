import torch
import torch.nn as nn
import torch.nn.functional as F


def mlp(input_dim, hidden_dim, output_dim, hidden_depth, output_mod=None):
    if hidden_depth == 0:
        mods = [nn.Linear(input_dim, output_dim)]
    else:
        mods = [nn.Linear(input_dim, hidden_dim), nn.ReLU(inplace=True)]
        for i in range(hidden_depth - 1):
            mods += [nn.Linear(hidden_dim, hidden_dim), nn.ReLU(inplace=True)]
        mods.append(nn.Linear(hidden_dim, output_dim))
    if output_mod is not None:
        mods.append(output_mod)
    trunk = nn.Sequential(*mods)
    return trunk


class Swish(nn.Module):
    def __init__(self, learnable_beta=False):
        super().__init__()
        self.learnable_beta = learnable_beta
        if learnable_beta:
            self.beta = nn.Parameter(torch.ones(()), requires_grad=True)
        else:
            self.beta = None

    def forward(self, x):
        if self.learnable_beta:
            return x * torch.sigmoid(self.beta * x)
        else:
            return x * torch.sigmoid(x)


class Conv2dWS(nn.Conv2d):
    """
    Weight Standardization
    """
    def forward(self, x):
        weight = self.weight
        weight_mean = (
            weight.mean(dim=1, keepdim=True)
            .mean(dim=2, keepdim=True)
            .mean(dim=3, keepdim=True)
        )
        weight = weight - weight_mean
        std = weight.view(weight.size(0), -1).std(dim=1).view(-1, 1, 1, 1) + 1e-5
        weight = weight / std.expand_as(weight)
        return F.conv2d(
            x, weight, self.bias, self.stride, self.padding, self.dilation, self.groups
        )
