from classopt import ClassOpt
from classopt import config


def default(default, help=None):
    return config(long=True, default=default, help=help)


if __name__ == '__main__':
    class CLIArgs(ClassOpt):
        pass

    args = CLIArgs().from_args()
