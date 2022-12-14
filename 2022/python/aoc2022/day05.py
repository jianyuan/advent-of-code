from .utils import read_lines_from_file_iter


def get_data():
    n_stacks = 9
    stacks = [[] for _ in range(n_stacks)]

    lines_iter = read_lines_from_file_iter("day05.txt", strip=False)

    for line in lines_iter:
        if line[1] == "1":
            # Reached the bottom of the stacks
            break

        for i in range(n_stacks):
            letter = line[i * 4 + 1 : (i * 4) + 2].strip()
            if letter:
                stacks[i].insert(0, letter)

    # Empty line
    next(lines_iter)

    steps = []
    for line in lines_iter:
        match line.strip().split():
            case ["move", qty, "from", a, "to", b]:
                steps.append((int(qty), int(a) - 1, int(b) - 1))

    return stacks, steps


def part_1():
    stacks, steps = get_data()

    for qty, a, b in steps:
        for _ in range(qty):
            letter = stacks[a].pop()
            stacks[b].append(letter)

    return "".join(stack.pop() for stack in stacks if stack)


def part_2():
    stacks, steps = get_data()

    for qty, a, b in steps:
        new_stack = []
        for _ in range(qty):
            letter = stacks[a].pop()
            new_stack.append(letter)
        stacks[b].extend(new_stack[::-1])

    return "".join(stack.pop() for stack in stacks if stack)


def main():
    print("Part 1:", part_1())
    print("Part 2:", part_2())


if __name__ == "__main__":
    main()
