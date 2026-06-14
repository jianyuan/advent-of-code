import argparse

from utils import read_line

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Path to input file")


def main():
    args = parser.parse_args()
    data = read_line(args.input, cast=parse_line)

    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))


def parse_line(line: str) -> list[tuple[int, int]]:
    ranges = line.split(",")
    results = []
    for rng in ranges:
        start, end = map(int, rng.split("-"))
        results.append((start, end))
    return results


def part_1(data: list[tuple[int, int]]) -> int:
    answer = 0

    for start, end in data:
        for number in range(start, end + 1):
            number_str = str(number)
            if len(number_str) % 2 != 0:
                continue

            mid = len(number_str) // 2
            left = number_str[:mid]
            right = number_str[mid:]

            if left == right:
                answer += number

    return answer


def part_2(data: list[tuple[int, int]]) -> int:
    answer = 0

    for start, end in data:
        invalid_numbers = set()

        for number in range(start, end + 1):
            number_str = str(number)

            for length in range(1, len(number_str)):
                parts = set()
                i = 0

                while number_str[i : i + length]:
                    part = number_str[i : i + length]
                    parts.add(part)
                    i += length

                if len(parts) == 1:
                    invalid_numbers.add(number)

        answer += sum(invalid_numbers)

    return answer


if __name__ == "__main__":
    main()
