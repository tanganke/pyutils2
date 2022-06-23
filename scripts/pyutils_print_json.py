#! /usr/bin/env python3
from pyutils.io.json import json, print_json

if __name__ == '__main__':
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
    j = json.load(open(args.file, 'r'))
    print_json(j, indent=args.indent)
