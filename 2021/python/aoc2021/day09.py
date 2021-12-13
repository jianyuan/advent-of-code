from functools import reduce
from operator import mul

from .utils import read_lines_from_file


def parse_data(data: list[str]) -> list[list[int]]:
    grid: list[list[int]] = []
    for line in data:
        grid.append([int(c) for c in line])
    return grid


deltas = [
    # Up
    (0, -1),
    # Down
    (0, 1),
    # Left
    (-1, 0),
    # Right
    (1, 0),
]


def get_minimum_points(data: list[list[int]]) -> list[tuple[int, int]]:
    results: list[tuple[int, int]] = []

    for y in range(len(data)):
        for x in range(len(data[0])):
            this = data[y][x]

            neighbours: set[int] = set()
            for dx, dy in deltas:
                if 0 <= y + dy < len(data) and 0 <= x + dx < len(data[0]):
                    neighbours.add(data[y + dy][x + dx])

            if all(neighbour > this for neighbour in neighbours):
                results.append((x, y))

    return results


def part_1(data: list[list[int]]) -> int:
    result = 0
    points = get_minimum_points(data)
    for x, y in points:
        result += data[y][x] + 1
    return result


def part_2(data: list[list[int]]) -> int:
    visited: set[tuple[int, int]] = set()
    points = get_minimum_points(data)
    sizes: list[int] = []

    for point in points:
        size = 0

        queue = [point]
        while queue:
            x, y = queue.pop()
            if (x, y) in visited:
                continue

            size += 1
            this = data[y][x]

            for dx, dy in deltas:
                if 0 <= y + dy < len(data) and 0 <= x + dx < len(data[0]):
                    neighbour = data[y + dy][x + dx]
                    if neighbour != 9 and neighbour >= this:
                        queue.append((x + dx, y + dy))

            visited.add((x, y))

        sizes.append(size)

    return reduce(mul, sorted(sizes)[-3:])


def main():
    data = parse_data(read_lines_from_file("day09.txt"))
    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))


if __name__ == "__main__":
    main()
