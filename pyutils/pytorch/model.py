from typing import Iterable
import torch
import torch.nn as nn
import numpy as np

__all__ = ['make_mlp', 'count_model_parameters']

def count_model_parameters(module: nn.Module) -> np.int64:
    """Counts the number of parameters in a torch model."""
    n = sum([np.prod(p.shape) for p in module.parameters()])
    return n


def make_mlp(sizes: Iterable[int], activation: nn.Module = nn.ReLU, output_activation: nn.Module = nn.Identity) -> nn.Sequential:
    """
    Example:
    >>> mlp = make_mlp([64, 32, 32], nn.ReLU, nn.Softmax)
    >>> mlp
    Sequential(
        (0): Linear(in_features=64, out_features=32, bias=True)
        (1): ReLU()
        (2): Linear(in_features=32, out_features=32, bias=True)
        (3): Softmax(dim=None)
    )
    """
    layers = []
    for j in range(len(sizes)-1):
        act = activation if j < len(sizes)-2 else output_activation
        layers += [nn.Linear(sizes[j], sizes[j+1]), act()]
    return nn.Sequential(*layers)
