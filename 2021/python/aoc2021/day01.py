from more_itertools import windowed

from .utils import read_lines_from_file


def count_increasing(data: list[int]) -> int:
    ans = 0
    for a, b in windowed(data, 2):
        if a < b:
            ans += 1
    return ans


def part_1(data: list[int]) -> int:
    return count_increasing(data)


def part_2(data: list[int]) -> int:
    new_data = [sum(xs) for xs in windowed(data, 3)]
    return count_increasing(new_data)


def main():
    data = read_lines_from_file("day01.txt", cast=int)
    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))


if __name__ == "__main__":
    main()
