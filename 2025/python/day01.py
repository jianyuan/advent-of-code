import argparse

from utils import read_lines

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Path to input file")


def main():
    args = parser.parse_args()
    data = read_lines(args.input, cast=parse_line)

    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))


def parse_line(line: str) -> tuple[str, int]:
    return line[0], int(line[1:])


def part_1(data: list[tuple[str, int]]) -> int:
    last = 50
    zeros = 0
    max = 100

    for direction, steps in data:
        step_change = -1 if direction == "L" else 1

        last += step_change * steps
        last %= max

        if last == 0:
            zeros += 1

    return zeros


def part_2(data: list[tuple[str, int]]) -> int:
    last = 50
    zeros = 0
    max = 100

    for direction, steps in data:
        step_change = -1 if direction == "L" else 1

        for _ in range(steps):
            last += step_change
            last %= max

            if last == 0:
                zeros += 1

    return zeros


if __name__ == "__main__":
    main()
