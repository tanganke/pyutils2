#! /usr/bin/env python3
import os
import sys
from pyutils.base import log
from pyutils.io.json import json, print_json
from pyutils.io import human_readable_size


def _error_exit(msg, ecode=1):
    log.error(msg)
    exit(ecode)


def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size


if __name__ == '__main__':
    log.set_log_level(log.LOG_LEVEL_INFO)

    def parse_args():
        from classopt import ClassOpt
        from classopt import config

        def default(default, help=None):
            return config(long=True, default=default, help=help)

        class Args(ClassOpt):
            file: str = config(default=None, help='path of json file')
            indent: str = config(short=True, long=True,
                                 default='  ', help='indent string')
            verbose: bool = config(short=True, long=True,
                                   default=False, help='is verbose? e.g. memory usage.')

        args = Args().from_args()
        return args

    args = parse_args()

    if not os.path.exists(args.file):
        _error_exit(f"File '{args.file}' not found.")
        exit(1)
    if not os.path.isfile(args.file):
        _error_exit(f"File '{args.file}' is not a file.")

    j = json.load(open(args.file, 'r'))

    # print file size
    log.info(
        f'file size: {human_readable_size(os.path.getsize(args.file), decimal_places=2)}')

    # print memory usage
    if args.verbose:
        log.info(
            f'loaded size in memory: {human_readable_size(get_size(j), decimal_places=2)}')

    # print key map
    log.info('key map:')
    print_json(j, indent=args.indent)
