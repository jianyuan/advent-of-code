from .utils import read_lines_from_file_iter


def get_data():
    data = []
    for line in read_lines_from_file_iter("day04.txt"):
        a, b = line.split(",")
        a1, a2 = a.split("-")
        b1, b2 = b.split("-")
        data.append((int(a1), int(a2), int(b1), int(b2)))
    return data


def fully_contains(a1, a2, b1, b2):
    return (a1 <= b1 and a2 >= b2) or (b1 <= a1 and b2 >= a2)


def part_1():
    data = get_data()
    return sum(int(fully_contains(*row)) for row in data)


def overlaps_at_all(a1, a2, b1, b2):
    return bool(set(range(a1, a2 + 1)) & set(range(b1, b2 + 1)))


def part_2():
    data = get_data()
    return sum(int(overlaps_at_all(*row)) for row in data)


def main():
    print("Part 1:", part_1())
    print("Part 2:", part_2())


if __name__ == "__main__":
    main()
