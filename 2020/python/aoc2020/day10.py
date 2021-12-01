from typing import Counter, Iterator

from .utils import read_lines_from_file


def part1(numbers: list[int]) -> int:
    def get_differences() -> Iterator[int]:
        for i in range(len(numbers) - 1):
            yield numbers[i + 1] - numbers[i]

    counter = Counter(get_differences())
    return counter[1] * counter[3]


def part2(numbers: list[int]) -> int:
    def get_choices_iter(index: int) -> Iterator[int]:
        current_number = numbers[index]
        index += 1
        while index < len(numbers) and numbers[index] - current_number <= 3:
            yield numbers[index]
            index += 1

    def get_choices(index: int) -> tuple[int, list[int]]:
        return numbers[index], list(get_choices_iter(index))

    number_choices = dict(get_choices(index) for index in range(len(numbers)))

    def count_choices(number: int, memo: dict[int, int]) -> int:
        if number in memo:
            return memo[number]

        memo[number] = sum(
            count_choices(choice, memo) for choice in number_choices[number]
        )

        return memo[number]

    return count_choices(0, {numbers[-1]: 1})


def main():
    numbers = read_lines_from_file("day10.txt", cast=int)
    numbers.sort()
    numbers.insert(0, 0)
    numbers.append(numbers[-1] + 3)

    print("Part 1:", part1(numbers))
    print("Part 2:", part2(numbers))


if __name__ == "__main__":
    main()
