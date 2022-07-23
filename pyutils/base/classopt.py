"""
parse CLI arguments:

.. code-block:: python

    from classopt import ClassOpt

    class CLIArgs(ClassOpt):
        from pyutils.base.classopt import config, default
        batch_size: int = default(64, help='batch_size')
    
    if __name__ == '__main__':
        args = CLIArgs().from_args()
        batch_size = args.batch_size

"""
from classopt import ClassOpt
from classopt import config 

config.__doc__ = \
"""
config an argument.

Args:
    long (Optional[bool], optional): _description_. Defaults to None.
    short (Optional[Union[bool, str]], optional): _description_. Defaults to None.
    action (Optional[str], optional): _description_. Defaults to None.
    nargs (Optional[Union[int, str]], optional): _description_. Defaults to None.
    const (Any, optional): _description_. Defaults to None.
    default (Any, optional): _description_. Defaults to None.
    type (Optional[type], optional): _description_. Defaults to None.
    choices (Optional[Iterable], optional): _description_. Defaults to None.
    required (Optional[bool], optional): _description_. Defaults to None.
    help (Optional[str], optional): _description_. Defaults to None.
    metavar (Optional[Union[str, Tuple[str]]], optional): _description_. Defaults to None.
    dest (Optional[str], optional): _description_. Defaults to None.
    version (Optional[str], optional): _description_. Defaults to None.
"""


def default(default, help=None):
    """
    Args:
        default (Any): default value
        help (str): help string.
    """
    return config(long=True, default=default, help=help)


if __name__ == '__main__':
    class CLIArgs(ClassOpt):
        pass

    args = CLIArgs().from_args()
