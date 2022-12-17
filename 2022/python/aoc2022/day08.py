from .utils import read_lines_from_file_iter


def get_data():
    data = []
    for line in read_lines_from_file_iter("day08.txt"):
        data.append([int(c) for c in line])
    return data


def part_1():
    data = get_data()
    x, y = len(data[0]), len(data)

    visible = 0

    for j in range(y):
        for i in range(x):
            value = data[j][i]
            if i == 0 or j == 0 or i == x - 1 or j == y - 1:
                # Edges
                visible += 1
            elif all(data[a][i] < value for a in range(j - 1, -1, -1)):
                # Top
                visible += 1
            elif all(data[a][i] < value for a in range(j + 1, y)):
                # Bottom
                visible += 1
            elif all(data[j][a] < value for a in range(i - 1, -1, -1)):
                # Left
                visible += 1
            elif all(data[j][a] < value for a in range(i + 1, x)):
                # Right
                visible += 1

    return visible


def part_2():
    data = get_data()
    x, y = len(data[0]), len(data)

    answer = 0

    for j in range(y):
        for i in range(x):
            value = data[j][i]
            if i == 0 or j == 0 or i == x - 1 or j == y - 1:
                # Edges
                pass
            else:
                result = 1

                for b, a in enumerate(range(j - 1, -1, -1)):
                    if data[a][i] >= value:
                        break
                result *= b + 1

                for b, a in enumerate(range(j + 1, y)):
                    if data[a][i] >= value:
                        break
                result *= b + 1

                for b, a in enumerate(range(i - 1, -1, -1)):
                    if data[j][a] >= value:
                        break
                result *= b + 1

                for b, a in enumerate(range(i + 1, x)):
                    if data[j][a] >= value:
                        break
                result *= b + 1

                answer = max(answer, result)
    return answer


def main():
    print("Part 1:", part_1())
    print("Part 2:", part_2())


if __name__ == "__main__":
    main()
