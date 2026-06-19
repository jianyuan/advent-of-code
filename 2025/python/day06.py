import functools
import argparse
import operator
from typing import Callable

from utils import read_lines

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Path to input file")

operator_map: dict[str, Callable[[int, int], int]] = {
    "+": operator.add,
    "*": operator.mul,
}


def main():
    args = parser.parse_args()
    lines = read_lines(args.input)

    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


def parse_data_1(lines: list[str]) -> tuple[list[list[int]], list[str]]:
    operators = lines[-1].split()
    numbers = [[int(s) for s in line.split()] for line in lines[:-1]]
    return numbers, operators


def part_1(lines: list[str]) -> int:
    numbers, operators = parse_data_1(lines)

    answer = sum(
        functools.reduce(operator_map[operators[i]], (col[i] for col in numbers))
        for i in range(len(operators))
    )

    return answer


def parse_data_2(lines: list[str]) -> tuple[list[list[int]], list[str]]:
    operators: list[str] = []
    widths: list[int] = []

    current_width = 0
    for c in lines[-1][::-1]:
        if c == " ":
            current_width += 1
        else:
            operators.append(c)
            widths.append(current_width + 1)
            current_width = -1

    numbers = [[] for _ in range(len(operators))]
    columns = lines[:-1]
    current_index = -1
    for i in range(len(operators)):
        width = widths[i]
        for j in range(width):
            current_number = ""
            for k in range(len(columns)):
                digit = columns[k][current_index]
                if digit.isdigit():
                    current_number += digit
            numbers[i].append(int(current_number))
            current_index -= 1
        current_index -= 1

    return numbers, operators


def part_2(lines: list[str]) -> int:
    numbers, operators = parse_data_2(lines)

    answer = sum(
        functools.reduce(operator_map[operators[i]], numbers[i])
        for i in range(len(operators))
    )

    return answer


if __name__ == "__main__":
    main()
