from typing import Iterator
import argparse

from utils import read_lines_iter

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Path to input file")


def main():
    args = parser.parse_args()
    ranges, ids = parse_data(read_lines_iter(args.input))

    print("Part 1:", part_1(ranges=ranges, ids=ids))
    print("Part 2:", part_2(ranges=ranges))


def parse_data(lines: Iterator[str]) -> tuple[list[tuple[int, int]], list[int]]:
    ranges: list[tuple[int, int]] = []
    ids: list[int] = []

    for line in lines:
        if line == "":
            break

        start, end = map(int, line.split("-"))
        ranges.append((start, end))

    for line in lines:
        ids.append(int(line))

    return ranges, ids


def part_1(*, ranges: list[tuple[int, int]], ids: list[int]) -> int:
    answer = 0

    for id in ids:
        for start, end in ranges:
            if start <= id <= end:
                answer += 1
                break

    return answer


def part_2(*, ranges: list[tuple[int, int]]) -> int:
    ranges = sorted(ranges)

    unique_ranges: list[tuple[int, int]] = [ranges[0]]
    for current in ranges[1:]:
        prev_start, prev_end = unique_ranges[-1]
        curr_start, curr_end = current

        if curr_start <= prev_end:
            unique_ranges[-1] = (prev_start, max(prev_end, curr_end))
        else:
            unique_ranges.append(current)

    answer = 0

    for start, end in unique_ranges:
        answer += end - start + 1

    return answer


if __name__ == "__main__":
    main()
