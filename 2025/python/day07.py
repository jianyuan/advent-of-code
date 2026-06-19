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


def part_1(lines: list[str]) -> int:
    start = lines[0].index("S")
    beams: set[int] = {start}

    splits = 0

    for line in lines[1:]:
        next_beams: set[int] = set()
        for beam in beams:
            if line[beam] == "^":
                splits += 1
                next_beams.add(beam - 1)
                next_beams.add(beam + 1)
            else:
                next_beams.add(beam)
        beams = next_beams

    return splits


def in_bounds(grid, x, y):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])


def get_char(grid, x, y):
    if in_bounds(grid, x, y):
        return grid[x][y]


def part_2(lines: list[str]) -> int:
    memo = {}

    def traverse(x: int, y: int):
        char = get_char(lines, x, y)
        if char is None:
            return 1

        if (x, y) in memo:
            return memo[(x, y)]

        if char == ".":
            result = traverse(x + 1, y)
        elif char == "^":
            result = traverse(x + 1, y - 1) + traverse(x + 1, y + 1)
        else:
            result = 0

        memo[(x, y)] = result
        return result

    return traverse(1, lines[0].index("S"))


if __name__ == "__main__":
    main()
