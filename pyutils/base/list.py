from typing import Iterable

__all__ = ['sorted_list']


def sorted_list(iter: Iterable) -> list:
    """
    convert iterable object `iter` to sorted list
    """
    ans = list(iter)
    ans.sort()
    return ans
