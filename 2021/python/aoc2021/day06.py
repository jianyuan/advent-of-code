from collections import Counter

from .utils import read_lines_from_file_iter


def simulate(data: list[int], *, days: int) -> int:
    state: Counter[int] = Counter(data)
    for _ in range(days):
        next_state: Counter[int] = Counter()
        for timer, count in state.items():
            if timer > 0:
                next_state[timer - 1] += count
            else:
                next_state[6] += count
                next_state[8] += count
        state = next_state
    return state.total()


def part_1(data: list[int]) -> int:
    return simulate(data, days=80)


def part_2(data: list[int]) -> int:
    return simulate(data, days=256)


def main():
    data = [
        int(number)
        for number in next(read_lines_from_file_iter("day06.txt")).split(",")
    ]
    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))


if __name__ == "__main__":
    main()
