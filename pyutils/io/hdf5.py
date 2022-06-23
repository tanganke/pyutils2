import h5py

__all__ = ['print_h5']


def print_h5(group, level=0):
    if(isinstance(group, h5py.Group) == False):
        print(level * '\t', group)
        return
    else:
        for key in group.keys():
            print(level * '\t' + key + ':')
            subgroup = group[key]
            print_h5(subgroup, level + 1)
