""" 
construct some simple models.
"""
import numpy as np
import torch
import torch.nn as nn
from typing import Iterable
from pyutils.base.arg import verify_str_arg


_activation_factory = {'relu': nn.ReLU, 'tanh': nn.Tanh,
                       'glu': nn.GLU, 'elu': nn.ELU,
                       'celu': nn.CELU, 'identity': nn.Identity}


def make_activation(name: str) -> nn.Module:
    """make activation layer by `name`

    Args:
        name (str): 'relu', 'tanh', 'glu', 'elu', 'celu' or 'identity'

    Returns:
        nn.Module: activation layer
    """
    verify_str_arg(name, 'name', _activation_factory.keys())
    return _activation_factory[name]()


def count_model_parameters(module: nn.Module) -> np.int64:
    """Counts the number of parameters in a torch model."""
    n = sum([np.prod(p.shape) for p in module.parameters()])
    return n


def make_mlp(sizes: Iterable[int],
             activation: nn.Module = nn.ReLU,
             output_activation: nn.Module = nn.Identity) -> nn.Sequential:
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
    for j in range(len(sizes) - 1):
        act = activation if j < len(sizes) - 2 else output_activation
        layers += [nn.Linear(sizes[j], sizes[j + 1]), act()]
    return nn.Sequential(*layers)


def make_LeNet(num_classes=10):
    """
    LeNet:
        input: (batch_size, 1, 28, 28)

    Args:
        num_classes (int, optional): _description_. Defaults to 10.

    Returns:
        nn.Module: LeNet
    """
    model = nn.Sequential(
        nn.Conv2d(1, 6, kernel_size=5, padding=2), nn.ReLU(),
        nn.MaxPool2d(kernel_size=2, stride=2),
        nn.Conv2d(6, 16, kernel_size=5), nn.ReLU(),
        nn.MaxPool2d(kernel_size=2, stride=2),
        nn.Flatten(),
        nn.Linear(16 * 5 * 5, 120), nn.ReLU(),
        nn.Linear(120, 84), nn.ReLU(),
        nn.Linear(84, num_classes))
    return model
