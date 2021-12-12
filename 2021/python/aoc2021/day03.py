from .utils import read_lines_from_file


def part_1(data: list[str]) -> int:
    n = len(data[0])
    gamma = 0
    for i in range(n):
        value = sum(row[i] == "1" for row in data) > len(data) / 2
        gamma += value << (n - 1 - i)
    epsilon = gamma ^ int("1" * n, 2)
    return gamma * epsilon


def part_2(data: list[str]) -> int:
    n = len(data[0])

    oxygen = data.copy()
    for i in range(n):
        value = sum(row[i] == "1" for row in oxygen) >= len(oxygen) / 2
        oxygen = [candidate for candidate in oxygen if int(candidate[i]) == value]
        if len(oxygen) == 1:
            break

    co2 = data.copy()
    for i in range(n):
        value = sum(row[i] == "1" for row in co2) < len(co2) / 2
        co2 = [candidate for candidate in co2 if int(candidate[i]) == value]
        if len(co2) == 1:
            break

    return int(oxygen[0], 2) * int(co2[0], 2)


def main():
    data = read_lines_from_file("day03.txt")
    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))


if __name__ == "__main__":
    main()
