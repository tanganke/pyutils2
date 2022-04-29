import sys
import warnings

"""A set of common utilities used within the environments. These are
not intended as API functions, and will not remain stable over time.
"""

__all__ = [
    'LOG_LEVEL_DEBUG', 'LOG_LEVEL_INFO', 'LOG_LEVEL_WARN', 'LOG_LEVEL_ERROR', 'LOG_LEVEL_DISABLED',
    'set_log_level', 'debug', 'info', 'warn', 'deprecation', 'error'
]

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

