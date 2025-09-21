import argparse
import re

import numpy as np

from utils import read_lines

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Path to input file")


def parse_line(line: str) -> list[int]:
    return [int(part) for part in re.split(r"\s+", line)]


def part_1(x):
    x = np.sort(x, axis=0)
    x = np.diff(x, axis=1)
    x = np.abs(x)
    return np.sum(x)


def part_2(x):
    x = np.transpose(x)
    labels, counts = np.unique_counts(x[1])
    label_to_count = {label: count for label, count in zip(labels, counts)}
    result = np.array([v * label_to_count.get(v, 0) for v in x[0]])
    return np.sum(result)


def main():
    args = parser.parse_args()
    x = np.array(read_lines(args.input, cast=parse_line))

    print("Part 1:", part_1(x))
    print("Part 2:", part_2(x))


if __name__ == "__main__":
    main()
