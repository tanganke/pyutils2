import os
import sys
import time
import warnings
from itertools import count

"""A set of common utilities used within the environments. These are
not intended as API functions, and will not remain stable over time.
"""

_color2num = dict(
    gray=30,
    red=31,
    green=32,
    yellow=33,
    blue=34,
    magenta=35,
    cyan=36,
    white=37,
    crimson=38,
)


def _colorize(string, color, bold=False, highlight=False):
    """Return string surrounded by appropriate terminal color codes to
    print colorized text.  Valid colors: gray, red, green, yellow,
    blue, magenta, cyan, white, crimson
    """

    attr = []
    num = _color2num[color]
    if highlight:
        num += 10
    attr.append(str(num))
    if bold:
        attr.append("1")
    attrs = ";".join(attr)
    return "\x1b[%sm%s\x1b[0m" % (attrs, string)


LOG_LEVEL_DEBUG = 10
LOG_LEVEL_INFO = 20
LOG_LEVEL_WARN = 30
LOG_LEVEL_ERROR = 40
LOG_LEVEL_DISABLED = 50

_MIN_LEVEL = 10


def set_log_level(level=LOG_LEVEL_DEBUG):
    """Set logging threshold on current logger.
    Args:
        level (int): 
            one of ``LOG_LEVEL_DEBUG``, ``LOG_LEVEL_INFO``, 
            ``LOG_LEVEL_WARN``, ``LOG_LEVEL_ERROR``, ``LOG_LEVEL_DISABLED``.
            Defaults to ``LOG_LEVEL_DEBUG``.
    """
    global _MIN_LEVEL
    _MIN_LEVEL = level


def debug(msg):
    if _MIN_LEVEL <= LOG_LEVEL_DEBUG:
        print(
            _colorize("%s: %s" % ("DEBUG", msg), 'blue'),
            file=sys.stderr
        )


def info(msg):
    if _MIN_LEVEL <= LOG_LEVEL_INFO:
        print(
            _colorize("%s: %s" % ("INFO", msg), 'green'),
            file=sys.stderr
        )


def warn(msg, category=None, stacklevel=1):
    if _MIN_LEVEL <= LOG_LEVEL_WARN:
        warnings.warn(
            _colorize("%s: %s" % ("WARN", msg), "yellow"),
            category=category,
            stacklevel=stacklevel + 1,
        )


def deprecation(msg):
    warn(msg, category=DeprecationWarning, stacklevel=2)


def error(msg):
    if _MIN_LEVEL <= LOG_LEVEL_ERROR:
        print(_colorize("%s: %s" % ("ERROR", msg), "red"), file=sys.stderr)


def create_log_dir(log_dir: str, try_backup=True) -> None:
    if os.path.exists(log_dir):
        if try_backup:
            if os.path.isdir(log_dir):
                for i in count(1):
                    backup_dir = f"{log_dir}.{i}"
                    if not os.path.exists(backup_dir):
                        break
                os.rename(log_dir, backup_dir)
                warn(f"{log_dir} exists, backup to {backup_dir}")
            else:
                raise ValueError(f"{log_dir} exists and is not a directory")
        else:
            raise ValueError(f"{log_dir} exists")
    os.makedirs(log_dir, exist_ok=False)
    pass


class TimeIt:
    def __init__(self, description: str = None, logger=info):
        self.logger = logger
        self.description = description if description is not None else 'timeit'

    def __enter__(self):
        self.start = time.time()
        self.logger(f'[start] {self.description}')

    def __exit__(self, exc_type, exc_value, tb):
        self.logger(f'[end] {self.description}: {(time.time()-self.start):.2f}s')


def log_args(args) -> None:
    """
    log CLI arguments to the screen.

    Args:
        args (argparse.Namespace): CLI arguments.
    """
    head = 'CLI arguments:\n'
    msg = ''
    for key in vars(args):
        msg += f'{key} = {getattr(args,key)}\n'
    info(head + msg)


def log_cmd(file: str = None) -> str:
    """
    log cmd

    Args:
        file(str): if file is not None, append to it with a timestamp. 
    """
    cmd = ' '.join(sys.argv)
    if file is not None:
        if not os.path.exists(os.path.dirname(file)):
            os.makedirs(os.path.dirname(file))
        with open(file, 'a') as f:
            f.write(f'[{time.ctime()}] ' + cmd + '\n')
