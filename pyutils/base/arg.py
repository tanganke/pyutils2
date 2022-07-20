from typing import Iterable, TypeVar, Optional

__all__ = ['verify_str_arg']


def iterable_to_str(iterable: Iterable) -> str:
    return "'" + "', '".join([str(item) for item in iterable]) + "'"


T = TypeVar("T", str, bytes)


def verify_str_arg(
    value: T,
    arg: Optional[str] = None,
    valid_values: Iterable[T] = None,
    custom_msg: Optional[str] = None,
) -> T:
    """

    Examples:
        if you have a function `f` accept `batch_size` as argument, such as:

            f(batch_size='half')

        >>> verify_str_arg(batch_size, 'batch_size', ['half', 'full'])

    Args:
        value (T): 
        arg (Optional[str], optional): . Defaults to None.
        valid_values (Iterable[T], optional): . Defaults to None.
        custom_msg (Optional[str], optional): . Defaults to None.

    Raises:
        ValueError: 

    Returns:
        T: value
    """
    if not isinstance(value, (str, bytes)):
        if arg is None:
            msg = "Expected type str, but got type {type}."
        else:
            msg = "Expected type str for argument {arg}, but got type {type}."
        msg = msg.format(type=type(value), arg=arg)
        raise ValueError(msg)

    if valid_values is None:
        return value

    if value not in valid_values:
        if custom_msg is not None:
            msg = custom_msg
        else:
            msg = "Unknown value '{value}' for argument {arg}. Valid values are {{{valid_values}}}."
            msg = msg.format(value=value, arg=arg,
                             valid_values=iterable_to_str(valid_values))
        raise ValueError(msg)

    return value
