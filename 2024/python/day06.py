import argparse
import dataclasses
import re
from copy import deepcopy
from typing import Self

from utils import read_lines

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Path to input file")


@dataclasses.dataclass(frozen=True, slots=True)
class Coordinate:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return self.__class__(self.x + other.x, self.y + other.y)


# UP > RIGHT > DOWN > LEFT
direction_indicators = ["^", ">", "v", "<"]
direction_deltas = [
    Coordinate(-1, 0),
    Coordinate(0, 1),
    Coordinate(1, 0),
    Coordinate(0, -1),
]


def parse_grid(lines: list[str]) -> tuple[list[list[str]], Coordinate, int]:
    grid = [list(line) for line in lines]
    rows, cols = len(grid), len(grid[0])
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] in direction_indicators:
                start = Coordinate(x, y)
                facing = direction_indicators.index(grid[x][y])
                grid[x][y] = "."  # Clear guard marker
                return grid, start, facing
    raise RuntimeError


def part_1(grid: list[list[str]], start: Coordinate, facing: int):
    rows, cols = len(grid), len(grid[0])
    visited: set[Coordinate] = set()
    current = start
    while 0 <= current.x < rows and 0 <= current.y < cols:
        visited.add(current)

        delta = direction_deltas[facing]
        new = current + delta
        if 0 <= new.x < rows and 0 <= new.y < cols and grid[new.x][new.y] == "#":
            facing = (facing + 1) % len(direction_indicators)
        else:
            current = new

    return len(visited)


def simulate_with_obstacle(
    grid: list[list[str]], start: Coordinate, facing: int, block: Coordinate
):
    test_grid = deepcopy(grid)
    test_grid[block.x][block.y] = "#"
    rows, cols = len(test_grid), len(test_grid[0])

    visited: set[tuple[Coordinate, int]] = set()
    current = start
    while 0 <= current.x < rows and 0 <= current.y < cols:
        if (current, facing) in visited:
            return True

        visited.add((current, facing))

        delta = direction_deltas[facing]
        new = current + delta
        if 0 <= new.x < rows and 0 <= new.y < cols and test_grid[new.x][new.y] == "#":
            facing = (facing + 1) % len(direction_indicators)
        else:
            current = new

    return False


def part_2(grid: list[list[str]], start: Coordinate, facing: int):
    rows, cols = len(grid), len(grid[0])

    count = 0
    for x in range(rows):
        for y in range(cols):
            if start == Coordinate(x, y) or grid[x][y] == "#":
                continue
            if simulate_with_obstacle(grid, start, facing, Coordinate(x, y)):
                count += 1
    return count


def main():
    args = parser.parse_args()
    grid, start, facing = parse_grid(read_lines(args.input))

    print("Part 1:", part_1(grid, start, facing))
    print("Part 2:", part_2(grid, start, facing))


if __name__ == "__main__":
    main()
