from .utils import read_lines_from_file_iter


def get_data():
    elves: list[list[int]] = []
    current_elf = []

    for line in read_lines_from_file_iter("day01.txt"):
        if line:
            current_elf.append(int(line))
        else:
            elves.append(current_elf)
            current_elf = []
    if current_elf:
        elves.append(current_elf)

    return elves


def part_1(data: list[list[int]]) -> int:
    return max(sum(calories) for calories in data)


def part_2(data: list[list[int]]) -> int:
    return sum(sorted((sum(calories) for calories in data), reverse=True)[:3])


def main():
    data = get_data()
    print("Part 1:", part_1(data))
    print("Part 1:", part_2(data))


if __name__ == "__main__":
    main()
