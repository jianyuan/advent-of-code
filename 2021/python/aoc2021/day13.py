from typing import Iterator

from .utils import read_lines_from_file_iter


def parse_data(
    data: Iterator[str],
) -> tuple[set[tuple[int, int]], list[tuple[str, int]]]:
    dots: set[tuple[int, int]] = set()
    folds: list[tuple[str, int]] = []

    for line in data:
        if not line:
            break
        x, y = line.split(",")
        dots.add((int(x), int(y)))

    for line in data:
        if line.startswith("fold along "):
            axis, value = line[len("fold along ") :].split("=")
            folds.append((axis, int(value)))

    return dots, folds


def calculate_dots(
    dots: set[tuple[int, int]],
    folds: list[tuple[str, int]],
    *,
    return_first: bool = False,
) -> set[tuple[int, int]]:
    x_size = max(x for x, _ in dots) + 1
    y_size = max(y for _, y in dots) + 1

    for axis, value in folds:
        new_dots: set[tuple[int, int]] = set()

        if axis == "y":
            for x, y in dots:
                if y > value:
                    new_dots.add((x, y_size - 1 - y))
                else:
                    new_dots.add((x, y))
            y_size = value
        else:
            for x, y in dots:
                if x > value:
                    new_dots.add((x_size - 1 - x, y))
                else:
                    new_dots.add((x, y))
            x_size = value

        dots = new_dots

        if return_first:
            break

    return dots


def part_1(dots: set[tuple[int, int]], folds: list[tuple[str, int]]) -> int:
    return len(calculate_dots(dots, folds, return_first=True))


def part_2(dots: set[tuple[int, int]], folds: list[tuple[str, int]]) -> str:
    final_dots = calculate_dots(dots, folds)
    x_size = max(x for x, _ in final_dots) + 1
    y_size = max(y for _, y in final_dots) + 1

    return "\n".join(
        "".join("#" if (x, y) in final_dots else "." for x in range(x_size))
        for y in range(y_size)
    )


def main():
    dots, folds = parse_data(read_lines_from_file_iter("day13.txt"))
    print("Part 1:", part_1(dots, folds))
    print("Part 2:")
    print(part_2(dots, folds))


if __name__ == "__main__":
    main()
