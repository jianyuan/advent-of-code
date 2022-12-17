from .utils import read_lines_from_file_iter


def get_data():
    data = []
    for line in read_lines_from_file_iter("day10.txt"):
        parts = line.split()
        if len(parts) == 2:
            parts[1] = int(parts[1])
        data.append(parts)
    return data


def part_1():
    data = get_data()

    x = 1
    cycle = 0

    strengths = []
    instruction_cycles = {
        "noop": 1,
        "addx": 2,
    }

    for instruction in data:
        for _ in range(instruction_cycles[instruction[0]]):
            cycle += 1
            if (cycle - 20) % 40 == 0:
                strengths.append(x * cycle)

        if instruction[0] == "addx":
            x += instruction[1]

    return sum(strengths[:6])


def part_2():
    data = get_data()

    w, h = 40, 6

    x = 1
    cycle = 0

    screen = ["."] * w * h
    instruction_cycles = {
        "noop": 1,
        "addx": 2,
    }

    for instruction in data:
        for _ in range(instruction_cycles[instruction[0]]):
            if cycle % w in {x - 1, x, x + 1}:
                screen[cycle] = "#"

            cycle += 1

        if instruction[0] == "addx":
            x += instruction[1]

    return "\n" + "\n".join("".join(screen[w * j : w * (j + 1)]) for j in range(h))


def main():
    print("Part 1:", part_1())
    print("Part 2:", part_2())


if __name__ == "__main__":
    main()
