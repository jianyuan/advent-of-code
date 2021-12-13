from copy import deepcopy

from .utils import read_lines_from_file


def parse_data(data: list[str]) -> list[list[int]]:
    grid: list[list[int]] = []
    for line in data:
        grid.append([int(c) for c in line])
    return grid


deltas = [
    # N
    (0, -1),
    # NW
    (-1, -1),
    # W
    (-1, 0),
    # SW
    (-1, 1),
    # S
    (0, 1),
    # SE
    (1, 1),
    # E
    (1, 0),
    # NE
    (1, -1),
]


def part_1(data: list[list[int]]) -> int:
    state = deepcopy(data)

    steps = 100
    flashes = 0
    for _ in range(steps):
        stack = [(x, y) for y in range(len(state)) for x in range(len(state[0]))]
        flashed: set[tuple[int, int]] = set()

        while stack:
            x, y = stack.pop()

            state[y][x] += 1
            if state[y][x] > 9 and (x, y) not in flashed:
                for dx, dy in deltas:
                    if 0 <= y + dy < len(state) and 0 <= x + dx < len(state[0]):
                        stack.append((x + dx, y + dy))

                flashes += 1
                flashed.add((x, y))

        for y in range(len(state)):
            for x in range(len(state[0])):
                if state[y][x] > 9:
                    state[y][x] = 0

    return flashes


def part_2(data: list[list[int]]) -> int:
    state = deepcopy(data)

    step = 0
    while True:
        step += 1

        stack = [(x, y) for y in range(len(state)) for x in range(len(state[0]))]
        flashed: set[tuple[int, int]] = set()

        while stack:
            x, y = stack.pop()

            state[y][x] += 1
            if state[y][x] > 9 and (x, y) not in flashed:
                for dx, dy in deltas:
                    if 0 <= y + dy < len(state) and 0 <= x + dx < len(state[0]):
                        stack.append((x + dx, y + dy))
                flashed.add((x, y))

        for y in range(len(state)):
            for x in range(len(state[0])):
                if state[y][x] > 9:
                    state[y][x] = 0

        if len(flashed) == len(data) * len(data[0]):
            return step


def main():
    data = parse_data(read_lines_from_file("day11.txt"))
    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))


if __name__ == "__main__":
    main()
