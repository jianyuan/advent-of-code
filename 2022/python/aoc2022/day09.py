from .utils import read_lines_from_file_iter


def get_data():
    data = []
    for line in read_lines_from_file_iter("day09.txt"):
        direction, value = line.split(" ")
        data.append((direction, int(value)))
    return data


def render(points, x, y):
    for j in range(y - 1, -1, -1):
        for i in range(x):
            print(points.get((i, j), "."), end="")
        print()
    print()


def part_1():
    data = get_data()

    head = (0, 0)
    tail = (0, 0)
    seen = set()

    instructions = data[::-1]
    while instructions:
        direction, value = instructions.pop()

        # print("Direction", direction, value)

        for _ in range(value):
            previous_head = head
            match direction:
                case "L":
                    head = (head[0] - 1, head[1])
                case "R":
                    head = (head[0] + 1, head[1])
                case "U":
                    head = (head[0], head[1] + 1)
                case "D":
                    head = (head[0], head[1] - 1)

            should_move = abs(head[0] - tail[0]) == 2 or abs(head[1] - tail[1]) == 2
            if should_move:
                tail = previous_head

            seen.add(tail)
            # render({head: "H", tail: "T"}, 6, 5)
            # render({point: "#" for point in seen}, 6, 5)

    return len(seen)


def part_2():
    data = get_data()

    points = [(0, 0)] * 10
    seen = set()

    instructions = data[::-1]
    while instructions:
        direction, value = instructions.pop()

        for _ in range(value):
            head = points[0]
            match direction:
                case "L":
                    head = (head[0] - 1, head[1])
                case "R":
                    head = (head[0] + 1, head[1])
                case "U":
                    head = (head[0], head[1] + 1)
                case "D":
                    head = (head[0], head[1] - 1)
            points[0] = head

            previous_point = points[0]
            for i in range(1, len(points)):
                point = points[i]
                if (
                    abs(previous_point[0] - point[0]) == 2
                    and abs(previous_point[1] - point[1]) == 2
                ):
                    # Diagonal
                    points[i] = (
                        (previous_point[0] + point[0]) // 2,
                        (previous_point[1] + point[1]) // 2,
                    )
                elif abs(previous_point[0] - point[0]) == 2:
                    # Left/Right
                    points[i] = ((previous_point[0] + point[0]) // 2, previous_point[1])
                elif abs(previous_point[1] - point[1]) == 2:
                    # Up/Down
                    points[i] = (previous_point[0], (previous_point[1] + point[1]) // 2)

                previous_point = points[i]

            seen.add(points[-1])

    return len(seen)


def main():
    print("Part 1:", part_1())
    print("Part 2:", part_2())


if __name__ == "__main__":
    main()
