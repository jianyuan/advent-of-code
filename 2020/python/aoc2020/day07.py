from parsy import regex, seq, string, whitespace

from .utils import read_lines_from_file


whitespace = regex(r"\s*")
lexeme = lambda p: p << whitespace
comma = lexeme(string(","))
integer = lexeme(regex(r"\d+")).map(int)
contain = lexeme(regex(r"contains?"))
bag = lexeme(regex(r"bags?"))
bag_color = lexeme(regex(r"\w+ \w+"))
no_other_bag = lexeme(string("no other")) + bag
content = seq(
    bag_color << bag << contain,
    (
        no_other_bag.result([])
        | seq(integer, bag_color << bag)
        .combine(lambda number, color: (color, number))
        .sep_by(comma)
    ).map(dict)
    << string("."),
)


def part1(rules):
    bag_queue = ["shiny gold"]
    result = set()

    while bag_queue:
        current_bag = bag_queue.pop()

        for bag, bag_contains in rules.items():
            if current_bag in bag_contains:
                bag_queue.append(bag)
                result.add(bag)

    return len(result)


def part2(rules):
    bag_queue = [(1, "shiny gold")]
    result = -1

    while bag_queue:
        quantity, current_bag = bag_queue.pop()

        bag = rules[current_bag]
        result += quantity

        for bag_contain, quantity_contain in bag.items():
            bag_queue.append((quantity * quantity_contain, bag_contain))

    return result


if __name__ == "__main__":
    example_rules = dict(read_lines_from_file("day07_example.txt", cast=content.parse))
    rules = dict(read_lines_from_file("day07.txt", cast=content.parse))

    print(part1(example_rules))
    print(part2(example_rules))

    print(part1(rules))
    print(part2(rules))
