import heapq

from .utils import read_lines_from_file_iter


def get_data():
    levels = {}
    start = None
    end = None

    for y, line in enumerate(read_lines_from_file_iter("day12.txt")):
        for x, letter in enumerate(line):
            if letter == "S":
                start = (x, y)
                letter = "a"
            elif letter == "E":
                end = (x, y)
                letter = "z"
            levels[(x, y)] = ord(letter) - ord("a")

    return levels, start, end


def get_neighbours(current):
    x, y = current
    yield x + 1, y
    yield x - 1, y
    yield x, y + 1
    yield x, y - 1


def part_1():
    data, start, end = get_data()
    candidates = [(0, start)]
    seen = set()

    while candidates:
        cost, current = heapq.heappop(candidates)
        if current == end:
            return cost

        if current in seen:
            continue
        seen.add(current)

        for neighbour in set(get_neighbours(current)) - seen:
            if neighbour in data and data[neighbour] - data[current] <= 1:
                heapq.heappush(candidates, (cost + 1, neighbour))


def part_2():
    data, _, end = get_data()

    candidates = []
    for coord, value in data.items():
        if value == 0:
            candidates.append((0, coord))

    seen = set()

    while candidates:
        cost, current = heapq.heappop(candidates)
        if current == end:
            return cost

        if current in seen:
            continue
        seen.add(current)

        for neighbour in set(get_neighbours(current)) - seen:
            if neighbour in data and data[neighbour] - data[current] <= 1:
                heapq.heappush(candidates, (cost + 1, neighbour))


def main():
    print("Part 1:", part_1())
    print("Part 2:", part_2())


if __name__ == "__main__":
    main()
