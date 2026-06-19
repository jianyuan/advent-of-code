from copy import deepcopy
import argparse

from utils import read_lines

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Path to input file")


def main():
    args = parser.parse_args()
    data = read_lines(args.input, cast=parse_line)

    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))


def parse_line(line: str) -> list[str]:
    return list(line)


directions = [
    [0, 1],
    [1, 0],
    [1, 1],
    [1, -1],
    [0, -1],
    [-1, 0],
    [-1, -1],
    [-1, 1],
]


def in_bounds(grid, x, y):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])


def get_char(grid, x, y):
    if in_bounds(grid, x, y):
        return grid[x][y]


def count_adjacent_rolls(grid, x, y):
    count = 0

    for dx, dy in directions:
        if get_char(grid, x + dx, y + dy) == "@":
            count += 1

    return count


def part_1(grid: list[str]) -> int:
    answer = 0

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if get_char(grid, x, y) == "@" and count_adjacent_rolls(grid, x, y) < 4:
                answer += 1

    return answer


def part_2(grid: list[str]) -> int:
    answer = 0

    while True:
        new_grid = deepcopy(grid)
        current_answer = 0

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if get_char(grid, x, y) == "@" and count_adjacent_rolls(grid, x, y) < 4:
                    new_grid[x][y] = "."
                    current_answer += 1

        if current_answer == 0:
            break

        grid = new_grid
        answer += current_answer

    return answer


if __name__ == "__main__":
    main()
