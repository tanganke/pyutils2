from typing import Iterable

def sorted_list(iter: Iterable) -> list:
    """
    convert iterable object `iter` to sorted list
    """
    ans = list(iter)
    ans.sort()
    return ans
