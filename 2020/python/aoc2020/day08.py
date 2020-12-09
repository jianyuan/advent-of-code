from typing import NamedTuple

from .utils import read_lines_from_file


def parse_instruction(line):
    instruction, value = line.split(" ", 2)
    return instruction, int(value)


class Result(NamedTuple):
    acc: int
    infinite_loop: bool


def run_instructions(instructions):
    seen = set()
    acc = 0
    pc = 0

    while True:
        if pc in seen:
            return Result(acc=acc, infinite_loop=True)
        elif pc == len(instructions):
            return Result(acc=acc, infinite_loop=False)

        seen.add(pc)

        instruction, value = instructions[pc]

        if instruction == "nop":
            pc += 1
        elif instruction == "acc":
            acc += value
            pc += 1
        elif instruction == "jmp":
            pc += value
        else:
            raise NotImplementedError


def iter_instructions_changes(instructions):
    for i in range(len(instructions)):
        instruction, value = instructions[i]
        if instruction in ("jmp", "nop"):
            current_instructions = instructions.copy()
            current_instructions[i] = ("nop" if instruction == "jmp" else "jmp", value)
            yield current_instructions


def part2(instructions):
    return next(
        result.acc
        for changed_instructions in iter_instructions_changes(instructions)
        if (result := run_instructions(changed_instructions))
        and not result.infinite_loop
    )


if __name__ == "__main__":
    example_instructions = read_lines_from_file(
        "day08_example.txt", cast=parse_instruction
    )
    instructions = read_lines_from_file("day08.txt", cast=parse_instruction)

    print(run_instructions(example_instructions))
    print(run_instructions(instructions))

    print(part2(example_instructions))
    print(part2(instructions))
