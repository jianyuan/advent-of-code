from dataclasses import dataclass

from .utils import read_lines_from_file


@dataclass
class Instruction:
    value: int


class Forward(Instruction):
    ...


class Up(Instruction):
    ...


class Down(Instruction):
    ...


def parse_instructions(data: list[str]) -> list[Instruction]:
    instructions: list[Instruction] = []
    for row in data:
        match row.split():
            case ["forward", value]:
                instructions.append(Forward(int(value)))
            case ["up", value]:
                instructions.append(Up(int(value)))
            case ["down", value]:
                instructions.append(Down(int(value)))
    return instructions


def part_1(instructions: list[Instruction]) -> int:
    h = depth = 0
    for instruction in instructions:
        match instruction:
            case Forward(value):
                h += value
            case Up(value):
                depth -= value
            case Down(value):
                depth += value
    return h * depth


def part_2(instructions: list[Instruction]) -> int:
    h = depth = aim = 0
    for instruction in instructions:
        match instruction:
            case Forward(value):
                h += value
                depth += aim * value
            case Up(value):
                aim -= value
            case Down(value):
                aim += value
    return h * depth


def main():
    data = read_lines_from_file("day02.txt")
    instructions = parse_instructions(data)
    print("Part 1:", part_1(instructions))
    print("Part 2:", part_2(instructions))


if __name__ == "__main__":
    main()
