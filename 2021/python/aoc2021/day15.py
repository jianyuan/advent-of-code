import heapq
from typing import Iterator

from .utils import read_lines_from_file_iter


def parse_map(lines: Iterator[str]):
    coords: dict[tuple[int, int], int] = {}
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            coords[(x, y)] = int(c)
    return coords


def expand_map(map: dict[tuple[int, int], int], by: int):
    w, h = max(map)

    def wrap(v: int):
        while v > 9:
            v -= 9
        return v

    return {
        (x + ((w + 1) * xs), y + ((h + 1) * ys)): wrap(v + xs + ys)
        for (x, y), v in map.items()
        for ys in range(by)
        for xs in range(by)
    }


def get_neighbours(current: tuple[int, int]) -> Iterator[tuple[int, int]]:
    x, y = current
    yield x + 1, y
    yield x - 1, y
    yield x, y + 1
    yield x, y - 1


def get_answer(map: dict[tuple[int, int], int]) -> int:
    origin, destination = min(map), max(map)
    candidates = [(0, origin)]
    seen: set[tuple[int, int]] = set()

    while candidates:
        cost, current = heapq.heappop(candidates)
        if current == destination:
            return cost

        if current in seen:
            continue
        seen.add(current)

        for neighbour in set(get_neighbours(current)) - seen:
            if neighbour in map:
                heapq.heappush(candidates, (cost + map[neighbour], neighbour))


def main():
    map = parse_map(read_lines_from_file_iter("day15.txt"))

    print("Part 1:", get_answer(map))
    print("Part 2:", get_answer(expand_map(map, by=5)))


if __name__ == "__main__":
    main()
