from .utils import read_lines_from_file


def count_trees(lines, move_x: int = 3, move_y: int = 1):
    y = len(lines)
    x = len(lines[0])

    i = 0
    j = 0

    count = 0

    while j < y - move_y:
        i += move_x
        i %= x
        j += move_y
        if lines[j][i] == "#":
            count += 1

    return count


def part_2(lines):
    return (
        count_trees(lines, move_x=1, move_y=1)
        * count_trees(lines, move_x=3, move_y=1)
        * count_trees(lines, move_x=5, move_y=1)
        * count_trees(lines, move_x=7, move_y=1)
        * count_trees(lines, move_x=1, move_y=2)
    )


if __name__ == "__main__":
    example_lines = read_lines_from_file("day03_example.txt")
    lines = read_lines_from_file("day03.txt")

    print(count_trees(example_lines))
    print(count_trees(lines))

    print(part_2(example_lines))
    print(part_2(lines))
