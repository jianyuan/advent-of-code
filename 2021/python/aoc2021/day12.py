from collections import Counter, defaultdict

from .utils import read_lines_from_file


def parse_data(data: list[str]) -> dict[str, set[str]]:
    paths: dict[str, set[str]] = defaultdict(set)
    for path in data:
        a, b = path.split("-")
        paths[a].add(b)
        paths[b].add(a)

    return paths


def count_paths(connections: dict[str, set[str]], *, limit: int) -> int:
    stack = [["start"]]
    paths: list[list[str]] = []

    while stack:
        path = stack.pop()
        visited = Counter(cave for cave in path if cave.islower())
        visit_limited = any(count == limit for count in visited.values())
        candidates = connections[path[-1]]

        for candidate in candidates:
            if candidate == "start":
                continue

            if candidate.islower() and visit_limited and candidate in visited:
                continue

            candidate_path = path + [candidate]
            if candidate == "end":
                paths.append(candidate_path)
            else:
                stack.append(candidate_path)

    return len(paths)


def part_1(connections: dict[str, set[str]]) -> int:
    return count_paths(connections, limit=1)


def part_2(connections: dict[str, set[str]]) -> int:
    return count_paths(connections, limit=2)


def main():
    data = parse_data(read_lines_from_file("day12.txt"))
    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))


if __name__ == "__main__":
    main()
