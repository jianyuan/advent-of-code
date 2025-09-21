import argparse
import dataclasses
from collections import defaultdict
from itertools import permutations
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

    def __sub__(self, other: Self) -> Self:
        return self.__class__(self.x - other.x, self.y - other.y)


def parse_grid(lines: list[str]) -> tuple[list[list[str]], dict[str, set[Coordinate]]]:
    grid = [list(line) for line in lines]
    rows, cols = len(grid), len(grid[0])
    antennas: dict[str, set[Coordinate]] = defaultdict(set)
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] != ".":
                antennas[grid[x][y]].add(Coordinate(x, y))
    return grid, antennas


def part_1(grid: list[list[str]], antennas: dict[str, set[Coordinate]]) -> int:
    rows, cols = len(grid), len(grid[0])
    antinodes: set[Coordinate] = set()
    for coordinates in antennas.values():
        pairs = permutations(coordinates, 2)
        for a, b in pairs:
            delta = a - b
            antinode = a + delta
            if (0 <= antinode.x < rows) and (0 <= antinode.y < cols):
                antinodes.add(antinode)
    return len(antinodes)


def part_2(grid: list[list[str]], antennas: dict[str, set[Coordinate]]):
    rows, cols = len(grid), len(grid[0])
    antinodes: set[Coordinate] = set()
    for coordinates in antennas.values():
        pairs = permutations(coordinates, 2)
        for a, b in pairs:
            antinodes.add(a)
            antinodes.add(b)
            delta = a - b
            current = a
            while 0 <= current.x < rows and 0 <= current.y < cols:
                antinodes.add(current)
                current += delta
    return len(antinodes)


def main():
    args = parser.parse_args()
    grid, antennas = parse_grid(read_lines(args.input))

    print("Part 1:", part_1(grid=grid, antennas=antennas))
    print("Part 2:", part_2(grid=grid, antennas=antennas))


if __name__ == "__main__":
    main()
