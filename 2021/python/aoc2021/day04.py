from dataclasses import dataclass
from itertools import islice
from typing import Iterator

from .utils import read_lines_from_file_iter


@dataclass
class Board:
    grid: list[list[int]]

    def is_bingo(self, numbers: list[int]) -> bool:
        # Row check
        for row in self.grid:
            if all(col in numbers for col in row):
                return True

        # Column check
        n = len(self.grid[0])
        for i in range(n):
            if all(row[i] in numbers for row in self.grid):
                return True

        return False

    def get_score(self, numbers: list[int]) -> int:
        unmarked_numbers = [
            col for row in self.grid for col in row if col not in numbers
        ]
        return sum(unmarked_numbers) * numbers[-1]


def parse_data(data: Iterator[str]) -> tuple[list[int], list[Board]]:
    numbers_line = next(data)
    numbers = [int(x) for x in numbers_line.split(",")]
    boards: list[Board] = []

    while True:
        try:
            # Empty line
            assert next(data) == ""
        except StopIteration:
            break
        grid = [[int(col) for col in row.split()] for row in islice(data, 5)]
        boards.append(Board(grid=grid))

    return numbers, boards


def part_1(numbers: list[int], boards: list[Board]) -> int:
    for i in range(len(numbers)):
        for board in boards:
            if board.is_bingo(numbers[:i]):
                return board.get_score(numbers[:i])
    raise RuntimeError


def part_2(numbers: list[int], boards: list[Board]) -> int:
    boards_remaining = boards.copy()
    last_winning_board: Board

    i = -1
    while boards_remaining:
        i += 1
        for j, board in enumerate(boards_remaining):
            if board.is_bingo(numbers[:i]):
                last_winning_board = boards_remaining.pop(j)

    return last_winning_board.get_score(numbers[:i])


def main():
    numbers, boards = parse_data(read_lines_from_file_iter("day04.txt"))
    print("Part 1:", part_1(numbers, boards))
    print("Part 2:", part_2(numbers, boards))


if __name__ == "__main__":
    main()
