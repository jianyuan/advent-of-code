import math
import operator

from .utils import read_file

operator_map = {"+": operator.add, "-": operator.sub, "*": operator.mul}


def get_data():
    notes = read_file("day11.txt").split("\n\n")

    data = []
    for note in notes:
        lines = note.splitlines()

        # Worry levels
        worry_levels = [
            int(number) for number in lines[1].split(": ", 1)[1].split(", ")
        ]

        # Operation
        raw_operator, raw_operand = lines[2].rsplit(" ", 2)[1:]
        operator = operator_map[raw_operator]
        operand = int(raw_operand) if raw_operand.isnumeric() else None

        # Test
        divisible_by = int(lines[3].rsplit(" ", 1)[-1])
        throw_to_if_true = int(lines[4].rsplit(" ", 1)[-1])
        throw_to_if_false = int(lines[5].rsplit(" ", 1)[-1])

        data.append(
            {
                "inspected": 0,
                "worry_levels": worry_levels,
                "operator": operator,
                "operand": operand,
                "divisible_by": divisible_by,
                "throw_to_if_true": throw_to_if_true,
                "throw_to_if_false": throw_to_if_false,
            }
        )

    return data


def part_1():
    data = get_data()

    for _ in range(20):
        for monkey in data:
            while monkey["worry_levels"]:
                monkey["inspected"] += 1

                worry_level = monkey["worry_levels"].pop(0)

                worry_level = monkey["operator"](
                    worry_level,
                    monkey["operand"] or worry_level,
                )

                worry_level //= 3

                if (worry_level % monkey["divisible_by"]) == 0:
                    data[monkey["throw_to_if_true"]]["worry_levels"].append(worry_level)
                else:
                    data[monkey["throw_to_if_false"]]["worry_levels"].append(
                        worry_level
                    )

    return math.prod(sorted(monkey["inspected"] for monkey in data)[-2:])


def part_2():
    data = get_data()

    lcm = math.prod(monkey["divisible_by"] for monkey in data)

    for _ in range(10_000):
        for monkey in data:
            while monkey["worry_levels"]:
                monkey["inspected"] += 1

                worry_level = monkey["worry_levels"].pop(0)

                worry_level = monkey["operator"](
                    worry_level,
                    monkey["operand"] or worry_level,
                )

                worry_level %= lcm

                if (worry_level % monkey["divisible_by"]) == 0:
                    data[monkey["throw_to_if_true"]]["worry_levels"].append(worry_level)
                else:
                    data[monkey["throw_to_if_false"]]["worry_levels"].append(
                        worry_level
                    )

    return math.prod(sorted(monkey["inspected"] for monkey in data)[-2:])


def main():
    print("Part 1:", part_1())
    print("Part 2:", part_2())


if __name__ == "__main__":
    main()
