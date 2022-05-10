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
