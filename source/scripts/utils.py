from itertools import zip_longest


def grouper(iterable, group_size):
    args = [iter(iterable)] * group_size

    return zip_longest(*args)
