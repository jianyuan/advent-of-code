import argparse

from utils import read_lines

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Path to input file")


def main():
    args = parser.parse_args()
    data = read_lines(args.input, cast=parse_line)

    print("Part 1:", get_answer(data, size=2))
    print("Part 2:", get_answer(data, size=12))


def parse_line(line: str) -> list[int]:
    return [int(i) for i in line]


def get_answer(banks: list[list[int]], size: int) -> int:
    answer = 0

    for bank in banks:
        start = 0

        for i in range(size):
            remaining_size = size - i

            end = len(bank) - remaining_size + 1
            search = bank[start:end]

            current_max = max(search)
            start += search.index(current_max) + 1

            answer += current_max * (10 ** (size - i - 1))

    return answer


if __name__ == "__main__":
    main()
