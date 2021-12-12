from itertools import permutations

from .utils import read_lines_from_file


def parse_data(data: list[str]) -> list[tuple[list[str], list[str]]]:
    entries: list[tuple[list[str], list[str]]] = []
    for entry in data:
        signals, outputs = entry.split(" | ")
        entries.append((signals.split(" "), outputs.split(" ")))
    return entries


def part_1(data: list[tuple[list[str], list[str]]]) -> int:
    count = 0
    for _, outputs in data:
        for output in outputs:
            if len(output) in {2, 4, 3, 7}:
                count += 1
    return count


def part_2(data: list[tuple[list[str], list[str]]]) -> int:
    display = "abcdefg"
    segments = {
        "abcefg": 0,
        "cf": 1,
        "acdeg": 2,
        "acdfg": 3,
        "bcdf": 4,
        "abdfg": 5,
        "abdefg": 6,
        "acf": 7,
        "abcdefg": 8,
        "abcdfg": 9,
    }

    def solve_output(signals: list[str], outputs: list[str]) -> int:
        for candidate in permutations(display):
            table = str.maketrans("".join(candidate), display)
            if all(
                "".join(sorted(signal.translate(table))) in segments
                for signal in signals
            ):
                return int(
                    "".join(
                        str(segments["".join(sorted(output.translate(table)))])
                        for output in outputs
                    )
                )
        raise RuntimeError

    result = 0
    for signals, outputs in data:
        result += solve_output(signals=signals, outputs=outputs)
    return result


def main():
    data = parse_data(read_lines_from_file("day08.txt"))
    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))


if __name__ == "__main__":
    main()
