from itertools import combinations, islice

from .utils import read_lines_from_file


def window(seq, n):
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for number in it:
        result = result[1:] + (number,)
        yield result


def part1(numbers, n):
    return next(
        numbers[-1]
        for numbers in window(numbers, n + 1)
        if all(
            sum(number_combinations) != numbers[-1]
            for number_combinations in combinations(numbers[:-1], 2)
        )
    )


def part2(numbers, n):
    invalid_number = part1(numbers, n)

    lo = 0
    acc = 0

    while lo < len(numbers):
        current_acc = numbers[lo]
        hi = lo + 1

        while hi < len(numbers):
            current_acc += numbers[hi]

            if current_acc == invalid_number:
                return min(numbers[lo:hi]) + max(numbers[lo:hi])
            elif current_acc > invalid_number:
                break

            hi += 1

        lo += 1


if __name__ == "__main__":
    example_numbers = read_lines_from_file("day09_example.txt", cast=int)
    numbers = read_lines_from_file("day09.txt", cast=int)

    print(part1(example_numbers, 5))
    print(part1(numbers, 25))

    print(part2(example_numbers, 5))
    print(part2(numbers, 25))
