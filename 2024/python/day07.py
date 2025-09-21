import argparse
import dataclasses
import operator
from itertools import product
from typing import Callable

from utils import read_lines

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Path to input file")


@dataclasses.dataclass(frozen=True, slots=True)
class Equation:
    result: int
    numbers: list[int]


def parse_line(line: str) -> Equation:
    raw_result, raw_numbers = line.split(": ", 1)
    return Equation(
        result=int(raw_result),
        numbers=[int(raw_number) for raw_number in raw_numbers.split(" ")],
    )


def get_result(
    equations: list[Equation],
    operations: list[Callable[[int, int], int]],
) -> int:
    answer = 0
    for equation in equations:
        possible_operators = product(
            *[operations for _ in range(len(equation.numbers) - 1)]
        )
        for operators in possible_operators:
            result = equation.numbers[0]
            for i, number in enumerate(equation.numbers[1:]):
                result = operators[i](result, number)
            if equation.result == result:
                answer += result
                break
    return answer


def part_1(equations: list[Equation]) -> int:
    return get_result(equations=equations, operations=[operator.add, operator.mul])


def concat_operator(a: int, b: int) -> int:
    return int(str(a) + str(b))


def part_2(equations: list[Equation]) -> int:
    return get_result(
        equations=equations, operations=[operator.add, operator.mul, concat_operator]
    )


def main():
    args = parser.parse_args()
    equations = read_lines(args.input, cast=parse_line)

    print("Part 1:", part_1(equations))
    print("Part 2:", part_2(equations))


if __name__ == "__main__":
    main()
