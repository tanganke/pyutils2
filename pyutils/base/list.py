from typing import Iterable


def sorted_list(iter: Iterable) -> list:
    """
    convert iterable object `iter` to sorted list
    """
    ans = list(iter)
    ans.sort()
    return ans


def list_ignore(iter: Iterable, ignore=None) -> list:
    """
    返回一个新列表，丢弃ignore指定的元素

    Args:
        iter (Iterable): _description_
        ignore (_type_, optional): _description_. Defaults to None.

    Returns:
        list
    """
    if ignore is None:
        return [item for item in iter if item is not None]
    else:
        return [item for item in iter if item in ignore]
