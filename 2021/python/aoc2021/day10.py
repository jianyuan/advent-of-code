from .utils import read_lines_from_file


points_1 = {")": 3, "]": 57, "}": 1197, ">": 25137}
points_2 = {")": 1, "]": 2, "}": 3, ">": 4}


class IllegalCharacter(ValueError):
    def __init__(self, character: str):
        self.character = character


def parse_syntax(syntax: str) -> list[str]:
    stack: list[str] = []
    for c in syntax:
        match c:
            case '(':
                stack.append(')')
            case '[':
                stack.append(']')
            case '{':
                stack.append('}')
            case '<':
                stack.append('>')
            case value:
                expected = stack.pop()
                if value != expected:
                    raise IllegalCharacter(value)
    return stack[::-1]


def part_1(data: list[str]) -> int:
    result = 0
    for line in data:
        try:
            parse_syntax(line)
        except IllegalCharacter as err:
            result += points_1[err.character]
    return result


def part_2(data: list[str]) -> int:
    incompletes: list[list[str]] = []
    for line in data:
        try:
            incomplete = parse_syntax(line)
        except IllegalCharacter:
            pass
        else:
            incompletes.append(incomplete)

    results: list[int] = []
    for incomplete in incompletes:
        score = 0
        for c in incomplete:
            score *= 5
            score += points_2[c]
        results.append(score)

    return sorted(results)[len(results) // 2]


def main():
    data = read_lines_from_file("day10.txt")
    print("Part 1:", part_1(data))
    print("Part 2:", part_2(data))


if __name__ == "__main__":
    main()
