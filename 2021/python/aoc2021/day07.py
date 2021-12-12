from .utils import read_lines_from_file_iter


def part_1(data: list[int]) -> int:
    min_position = min(data)
    max_position = max(data)
    return min(
        sum(abs(p - n) for p in data) for n in range(min_position, max_position + 1)
    )


def part_2(data: list[int]) -> int:
    min_position = min(data)
    max_position = max(data)
    return min(
        sum(abs(p - n) * (abs(p - n) + 1) // 2 for p in data)
        for n in range(min_position, max_position + 1)
    )


def main():
    data = [
        int(number)
        for number in next(read_lines_from_file_iter("day07.txt")).split(",")
    ]
    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))


if __name__ == "__main__":
    main()
