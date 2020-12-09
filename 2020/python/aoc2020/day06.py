import operator
from functools import reduce

from .utils import read_lines_from_file


def parse_groups(lines):
    groups = []
    current_group = []

    for line in lines:
        if line == "":
            groups.append(current_group)
            current_group = []
            continue

        current_group.append(set(line))

    groups.append(current_group)
    return groups


if __name__ == "__main__":
    groups = parse_groups(read_lines_from_file("day06.txt"))

    print(sum(len(reduce(operator.or_, group)) for group in groups))
    print(sum(len(reduce(operator.and_, group)) for group in groups))
