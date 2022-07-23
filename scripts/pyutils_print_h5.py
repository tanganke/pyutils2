#! /usr/bin/env python3
"""
usage: pyutils_print_h5.py [-h] [--indent INDENT] file

positional arguments:
  file                  path of hdf5 file

optional arguments:
  -h, --help            show this help message and exit
  --indent INDENT, -i INDENT
                        indent string 
"""
import os
import sys
from pyutils.base import log
from pyutils.io.hdf5 import h5py, print_h5
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
            file: str = config(default=None, help='path of hdf5 file')
            indent: str = config(short=True, long=True,
                                 default='  ', help='indent string')

        args = Args().from_args()
        return args

    args = parse_args()

    if not os.path.exists(args.file):
        _error_exit(f"File '{args.file}' not found.")
    if not os.path.isfile(args.file):
        _error_exit(f"File '{args.file}' is not a file.")

    h5_file = h5py.File(os.path.expanduser(args.file), 'r')

    # print file size
    log.info(
        f'file size: {human_readable_size(os.path.getsize(args.file), decimal_places=2)}')

    # print key map
    log.info('key map:')
    print_h5(h5_file)
