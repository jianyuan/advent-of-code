from .utils import read_lines_from_file_iter


def get_data():
    return next(read_lines_from_file_iter("day06.txt"))


def part_1():
    data = get_data()
    for i in range(len(data) - 3):
        if len(set(data[i : i + 4])) == 4:
            return i + 4


def part_2():
    data = get_data()
    for i in range(len(data) - 13):
        if len(set(data[i : i + 14])) == 14:
            return i + 14


def main():
    print("Part 1:", part_1())
    print("Part 2:", part_2())


if __name__ == "__main__":
    main()
