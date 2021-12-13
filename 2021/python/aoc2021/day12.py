import string
from collections import Counter, defaultdict

from .utils import read_lines_from_file


def parse_data(data: list[str]) -> dict[str, set[str]]:
    paths: dict[str, set[str]] = defaultdict(set)
    for path in data:
        a, b = path.split("-")
        paths[a].add(b)
        paths[b].add(a)

    return paths


def part_1(connections: dict[str, set[str]]) -> int:
    stack = [["start"]]
    paths: list[list[str]] = []

    while stack:
        path = stack.pop()
        visited = set(path)
        candidates = connections[path[-1]]

        for candidate in candidates:
            if candidate[0] in string.ascii_lowercase and candidate in visited:
                continue

            candidate_path = path + [candidate]
            if candidate == "end":
                paths.append(candidate_path)
            else:
                stack.append(candidate_path)

    return len(paths)


def part_2(connections: dict[str, set[str]]) -> int:
    stack = [["start"]]
    paths: list[list[str]] = []

    while stack:
        path = stack.pop()
        visited_small_caves = Counter(
            cave for cave in path if cave[0] in string.ascii_lowercase
        )
        visited_twice = any(count == 2 for count in visited_small_caves.values())
        candidates = connections[path[-1]]

        for candidate in candidates:
            if candidate == "start":
                continue

            if (
                candidate[0] in string.ascii_lowercase
                and visited_twice
                and candidate in visited_small_caves
            ):
                continue

            candidate_path = path + [candidate]
            if candidate == "end":
                paths.append(candidate_path)
            else:
                stack.append(candidate_path)

    return len(paths)


def main():
    data = parse_data(read_lines_from_file("day12.txt"))
    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))


if __name__ == "__main__":
    main()
