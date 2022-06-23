import h5py

__all__ = ['print_h5']


def print_h5(group, indent='  '):
    def _print_h5(group, level=0):
        if(isinstance(group, h5py.Group) == False):
            print(level * indent, group)
            return
        else:
            for key in group.keys():
                print(level * indent + key + ':')
                subgroup = group[key]
                _print_h5(subgroup, level + 1)

    _print_h5(group, 0)
