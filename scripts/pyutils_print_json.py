#! /usr/bin/env python3
import os
import sys
from pyutils.base import log
from pyutils.io.json import json, print_json
from pyutils.io import human_readable_size


def _error_exit(msg, ecode=1):
    log.error(msg)
    exit(ecode)


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

        args = Args().from_args()
        return args

    args = parse_args()
    if not os.path.exists(args.file):
        _error_exit(f"File '{args.file}' not found.")
        exit(1)
    if not os.path.isfile(args.file):
        _error_exit(f"File '{args.file}' is not a file.")

    j = json.load(open(args.file, 'r'))

    log.info(f'file size: {human_readable_size(os.path.getsize(args.file), decimal_places=2)}')
    log.info(f'loaded size in memory: {human_readable_size(sys.getsizeof(j), decimal_places=2)}')
    log.info('key map:')
    print_json(j, indent=args.indent)
