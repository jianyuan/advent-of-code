import argparse
import re

from utils import read_lines

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Path to input file")

mul_pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
mul_regex = re.compile(mul_pattern)
do_pattern = r"do\(\)"
dont_pattern = r"don't\(\)"


def parse_and_sum_muls(x):
    matches = mul_regex.findall(x)
    return sum(int(match[0]) * int(match[1]) for match in matches)


def parse_and_sum_muls_with_conditions(x):
    pattern = re.compile(rf"{mul_pattern}|{do_pattern}|{dont_pattern}")
    tokens = [m[0] for m in re.finditer(pattern, x)]

    enabled = True
    total = 0

    for token in tokens:
        if re.fullmatch(do_pattern, token):
            enabled = True
        elif re.fullmatch(dont_pattern, token):
            enabled = False
        else:
            m = mul_regex.fullmatch(token)
            if m and enabled:
                x, y = int(m[1]), int(m[2])
                total += x * y

    return total


def part_1(x):
    return parse_and_sum_muls(x)


def part_2(x):
    return parse_and_sum_muls_with_conditions(x)


def main():
    args = parser.parse_args()
    x = "".join(read_lines(args.input))

    print("Part 1:", part_1(x))
    print("Part 2:", part_2(x))


if __name__ == "__main__":
    main()
