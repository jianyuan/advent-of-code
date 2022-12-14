from .utils import read_lines_from_file_iter


def get_data():
    rounds = []
    for line in read_lines_from_file_iter("day02.txt"):
        a, b = line.split(" ")
        rounds.append((ord(a) - ord("A") + 1, ord(b) - ord("X") + 1))
    return rounds


def part_1():
    rounds = get_data()

    score = 0
    for a, b in rounds:
        score += b

        if a == b:
            score += 3
        elif (b - a) % 3 == 1:
            score += 6

    return score


def part_2():
    rounds = get_data()

    score = 0
    for a, b in rounds:
        score += (a + b) % 3 + 1
        score += (b - 1) * 3

    return score


def main():
    print("Part 1:", part_1())
    print("Part 2:", part_2())


if __name__ == "__main__":
    main()
