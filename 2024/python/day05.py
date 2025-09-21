import argparse
from collections import defaultdict
from graphlib import TopologicalSorter

from toolz import sliding_window

from utils import read_lines

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Path to input file")


def parse_input(lines) -> tuple[list[tuple[int, int]], list[list[int]]]:
    content = "\n".join(lines)
    raw_rules, raw_updates = content.split("\n\n")

    rules: list[tuple[int, int]] = []
    for raw_rule in raw_rules.split("\n"):
        a, b = [int(x) for x in raw_rule.split("|")]
        rules.append((a, b))

    updates: list[list[int]] = []
    for raw_update in raw_updates.split("\n"):
        updates.append([int(x) for x in raw_update.split(",")])

    return rules, updates


def is_correct_order(rules, update):
    pairs = list(sliding_window(2, update))
    matches = sum(pair in rules for pair in pairs)
    return matches == len(pairs)


def topological_sort(rules):
    graph: dict[int, set[int]] = defaultdict(set)
    for a, b in rules:
        graph[a].add(b)
    ts = TopologicalSorter(graph)
    return list(ts.static_order())


def part_1(rules, updates):
    total = 0
    for update in updates:
        if is_correct_order(rules, update):
            middle = update[len(update) // 2]
            total += middle
    return total


def part_2(rules, updates):
    incorrect_updates = []
    for update in updates:
        if not is_correct_order(rules, update):
            incorrect_updates.append(update)

    total = 0
    for update in incorrect_updates:
        subset_rules = [(a, b) for a, b in rules if a in update and b in update]
        sorted_update = topological_sort(subset_rules)
        middle = sorted_update[len(sorted_update) // 2]
        total += middle
    return total


def main():
    args = parser.parse_args()
    rules, updates = parse_input(read_lines(args.input))

    print("Part 1:", part_1(rules, updates))
    print("Part 2:", part_2(rules, updates))


if __name__ == "__main__":
    main()
