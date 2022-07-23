from typing import Iterable, TypeVar, Optional


def default(default_value, arg):
    r"""
    Return `default_value` if `arg` is `None`, else `arg`.

    Examples:

        set `batch_size` to 32 if `args.batch_size` is `None`, else `args.batch_size`

        .. code-block::

            batch_size = default(32, args.batch_size)

    Args:
        default_value (Any):
        arg (Any):
    """
    if arg is None:
        return default_value
    else:
        return arg


def _iterable_to_str(iterable: Iterable) -> str:
    return "'" + "', '".join([str(item) for item in iterable]) + "'"


T = TypeVar("T", str, bytes)


def verify_str_arg(
    value: T,
    arg: Optional[str] = None,
    valid_values: Iterable[T] = None,
    custom_msg: Optional[str] = None,
    to_lower: bool = False
) -> T:
    r"""
    check is string argument `value` with name `arg` in `valid_values`, raise `ValueError` if failed.

    Examples:
        if you have a function `f` accept `batch_size` as argument, such as:
        
        .. code-block::

            def f(batch_size='half'):
                verify_str_arg(batch_size, 'batch_size', ['half', 'full'])
                ...

    Args:
        value (T): 
        arg (Optional[str], optional): . Defaults to None.
        valid_values (Iterable[T], optional): Defaults to `None`. if this is `None`, accept any string input.
        custom_msg (Optional[str], optional): Defaults to "Unknown value '{value}' for argument {arg}. Valid values are {{{valid_values}}}.".
        to_lower(bool): if `True`, accept uppercase value.

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
    else:
        if valid_values is None:
            return value

        if to_lower:
            value = value.lower()

        if value not in valid_values:
            if custom_msg is not None:
                msg = custom_msg
            else:
                msg = "Unknown value '{value}' for argument {arg}. Valid values are {{{valid_values}}}."
                msg = msg.format(value=value, arg=arg,
                                 valid_values=_iterable_to_str(valid_values))
            raise ValueError(msg)

    return value
