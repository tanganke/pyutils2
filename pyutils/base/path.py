import os
from typing import List


def listdir_fullpath(dir: str) -> List[str]:
    """list directory `dir`, return fullpaths

    Args:
        dir (str): directory name

    Returns:
        List[str]: a list of fullpaths
    """
    assert os.path.isdir(dir), "Argument 'dir' must be a Directory"
    names = os.listdir(dir)
    return [os.path.join(dir, name) for name in names]


