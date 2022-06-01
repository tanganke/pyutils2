import re

RE_INT = '[+-]?[0-9]+'
"""
This will match integers:
- 123
- -123
"""
RE_FLOAT_NORMAL = '[+-]?([0-9]*[.])?[0-9]+'
"""
This will match:
- 123
- -123.456
- .456
"""
RE_FLOAT_SCITIFIC = f'{RE_FLOAT_NORMAL}[eE]{RE_INT}'
RE_FLOAT = f'(({RE_FLOAT_SCITIFIC})|({RE_FLOAT_NORMAL}))'


def re_tuple(*elements):
    R"""
    Args:
        elements: Regular expressions

    Returns:
        str: Regular expression matching a `tuple` of elements
    """
    return '\(\s*' + R',\s*'.join(elements) + (',\s*\)' if len(elements) <= 1 else '\s*\)')


def re_list(*elements):
    R"""
    Args:
        elements: Regular expressions

    Returns:
        str: Regular expression matching a `list` of elements
    """
    return '\[\s*' + R',\s*'.join(elements) + '\s*\]'


def re_from_expr(x):
    R"""
    Example:
        >>> re_int = '-?[0-9]+'
        >>> re_pattern = re_from_expr(((re_int, (re_int,)), (re_int, (re_int,)), (re_int,)))
        >>> re.match(re_pattern, '((-2146, (6,)), (1124, (97,)), (-1,))')
        <re.Match object; span=(0, 37), match='((-2146, (6,)), (1124, (97,)), (-1,))'>

    Args:
        x: Python object

    Returns:
        str: Regular expression
    """
    if isinstance(x, str):
        return x
    # types
    elif x == int:
        return RE_INT
    elif x == float:
        return RE_FLOAT
    # container
    elif isinstance(x, tuple):
        return re_tuple(*tuple(map(re_from_expr, x)))
    elif isinstance(x, list):
        return re_list(*tuple(map(re_from_expr, x)))
    else:
        raise NotImplementedError(
            're_from_expr: not implemented for type {}'.format(type(x)))
