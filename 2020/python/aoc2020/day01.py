from functools import reduce
from itertools import combinations
from operator import mul

from .utils import read_lines_from_file


def get_answer(numbers, *, take: int = 2):
    for combs in combinations(numbers, take):
        if sum(combs) == 2020:
            yield reduce(mul, combs)


if __name__ == "__main__":
    example_numbers = [1721, 979, 366, 299, 675, 1456]
    file_numbers = list(read_lines_from_file("day01.txt", cast=int))

    print(list(get_answer(example_numbers)))
    print(list(get_answer(file_numbers)))
    print(list(get_answer(example_numbers, take=3)))
    print(list(get_answer(file_numbers, take=3)))
