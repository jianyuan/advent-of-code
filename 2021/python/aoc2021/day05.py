from typing import NamedTuple, Optional

from .utils import read_lines_from_file


class Point(NamedTuple):
    x: int
    y: int


def full_range(start_or_stop: int, stop: Optional[int] = None):
    if stop is None:
        return range(start_or_stop + 1)
    else:
        return range(start_or_stop, stop + 1)


def parse_lines(data: list[str]) -> list[tuple[Point, Point]]:
    lines: list[tuple[Point, Point]] = []
    for row in data:
        from_, to = row.split(" -> ")
        from_x, from_y = from_.split(",")
        to_x, to_y = to.split(",")
        lines.append(
            tuple(
                sorted([Point(int(from_x), int(from_y)), Point(int(to_x), int(to_y))])
            )
        )
    return lines


def count_overlaps(lines: list[tuple[Point, Point]], *, supports_diagonal: bool) -> int:
    max_x = max(point.x for line in lines for point in line)
    max_y = max(point.y for line in lines for point in line)

    state = [[0 for _ in full_range(max_x)] for _ in full_range(max_y)]

    for a, b in lines:
        if a.x == b.x:
            for y in full_range(a.y, b.y):
                state[y][a.x] += 1
        elif a.y == b.y:
            for x in full_range(a.x, b.x):
                state[a.y][x] += 1
        elif supports_diagonal:
            y = a.y
            y_direction = -1 if a.y > b.y else 1
            for x in full_range(a.x, b.x):
                state[y][x] += 1
                y += y_direction

    return sum(1 for ys in state for x in ys if x > 1)


def part_1(lines: list[tuple[Point, Point]]) -> int:
    return count_overlaps(lines, supports_diagonal=False)


def part_2(lines: list[tuple[Point, Point]]) -> int:
    return count_overlaps(lines, supports_diagonal=True)


def main():
    data = read_lines_from_file("day05.txt")
    lines = parse_lines(data)
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == "__main__":
    main()
