from .common import *
from . import detect

from .device import *
from .model import *
from typing import Union


def random_seed(seed: Union[int, None], verbose=True):
    if seed is None:
        return

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)

    if verbose:
        log.info(f"setting random seed: {seed}")


def to_device(x: Tensor, y: Tensor) -> Tensor:
    """
    move `x` to `y.device` if x.device != y.device.
    """
    if x.device != y.device:
        x = x.to(y.device)
    return x
