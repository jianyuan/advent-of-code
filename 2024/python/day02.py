import argparse
import re

from toolz import sliding_window

from utils import read_lines

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Path to input file")


def parse_line(line: str) -> list[int]:
    return [int(part) for part in re.split(r"\s+", line)]


def is_safe(xs):
    pairs = list(sliding_window(2, xs))
    diffs = [b - a for a, b in pairs]
    all_pos = all(d > 0 for d in diffs)
    all_neg = all(d < 0 for d in diffs)

    def diffrange(x):
        return (-3 <= x <= -1) or (1 <= x <= 3)

    all_in_range = all(diffrange(d) for d in diffs)
    return (all_pos or all_neg) and all_in_range


def is_safe_with_dampener(xs):
    if is_safe(xs):
        return True
    for i in range(len(xs)):
        attempted = xs[:i] + xs[i + 1 :]
        if is_safe(attempted):
            return True
    return False


def part_1(x):
    return sum(is_safe(xs) for xs in x)


def part_2(x):
    return sum(is_safe_with_dampener(xs) for xs in x)


def main():
    args = parser.parse_args()
    x = read_lines(args.input, cast=parse_line)

    print("Part 1:", part_1(x))
    print("Part 2:", part_2(x))


if __name__ == "__main__":
    main()
