from .utils import read_lines_from_file


def get_data():
    return read_lines_from_file("day03.txt")


def get_priority(letter):
    if letter.islower():
        return ord(letter) - ord("a") + 1
    else:
        return ord(letter) - ord("A") + 27


def part_1():
    lines = get_data()

    result = 0
    for line in lines:
        letter = list(set(line[: len(line) // 2]) & set(line[len(line) // 2 :]))[0]
        result += get_priority(letter)
    return result


def part_2():
    lines = get_data()

    result = 0
    for i in range(len(lines) // 3):
        letter = list(
            set(lines[i * 3]) & set(lines[i * 3 + 1]) & set(lines[i * 3 + 2])
        )[0]
        result += get_priority(letter)
    return result


def main():
    print("Part 1:", part_1())
    print("Part 2:", part_2())


if __name__ == "__main__":
    main()
