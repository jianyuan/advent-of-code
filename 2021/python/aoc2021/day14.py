from collections import Counter
from typing import Iterator

from .utils import read_lines_from_file_iter


def parse_data(lines: Iterator[str]):
    template = next(lines)

    next(lines)  # empty line

    rules: dict[str, str] = {}
    for line in lines:
        pair, insert = line.split(" -> ")
        rules[pair] = insert

    return template, rules


def get_answer(*, template: str, rules: dict[str, str], steps: int) -> int:
    pairs = [template[i : i + 2] for i in range(len(template) - 1)]
    count_pairs = Counter(pairs)
    count_chars = Counter(template)

    for step in range(1, steps + 1):
        count_pairs_new = Counter()
        count_chars_new = Counter(template[-1])

        for pair, n in count_pairs.items():
            if rule := rules.get(pair):
                count_pairs_new[pair[0] + rule] += n
                count_pairs_new[rule + pair[1]] += n
                count_chars_new[pair[0]] += n
                count_chars_new[rule] += n

        count_pairs = count_pairs_new
        count_chars = count_chars_new

    common_chars = count_chars.most_common()
    return common_chars[0][1] - common_chars[-1][1]


def main():
    template, rules = parse_data(read_lines_from_file_iter("day14.txt"))

    print("Part 1:", get_answer(template=template, rules=rules, steps=10))
    print("Part 2:", get_answer(template=template, rules=rules, steps=40))


if __name__ == "__main__":
    main()
