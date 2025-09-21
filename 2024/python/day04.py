import argparse

from utils import read_lines

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Path to input file")


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


def get_letter(grid, x, y):
    if in_bounds(grid, x, y):
        return grid[x][y]


def search_xmas(grid, x, y, dx, dy):
    word = list("XMAS")
    letters = [get_letter(grid, x + (dx * i), y + (dy * i)) for i in range(len(word))]
    return letters == word


def count_xmas(grid):
    coords = [[x, y] for x in range(len(grid)) for y in range(len(grid[0]))]

    total = 0

    for x, y in coords:
        for dx, dy in directions:
            total += search_xmas(grid, x, y, dx, dy)

    return total


def part_1(x):
    return count_xmas(x)


def check_x_mas(grid, x, y):
    diag1 = [get_letter(grid, x + d, y + d) for d in [0, 1, 2]]
    diag2 = [get_letter(grid, x + 2 - d, y + d) for d in [0, 1, 2]]

    return (diag1 == list("MAS") or diag1 == list("SAM")) and (
        diag2 == list("MAS") or diag2 == list("SAM")
    )


def count_x_mas(grid):
    coords = [[x, y] for x in range(len(grid)) for y in range(len(grid[0]))]

    total = 0

    for x, y in coords:
        total += check_x_mas(grid, x, y)

    return total


def part_2(x):
    return count_x_mas(x)


def main():
    args = parser.parse_args()
    x = read_lines(args.input)

    print("Part 1:", part_1(x))
    print("Part 2:", part_2(x))


if __name__ == "__main__":
    main()
