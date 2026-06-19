import argparse

from utils import read_lines

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Path to input file")
parser.add_argument("--connections", type=int, default=1000)


def main():
    args = parser.parse_args()
    boxes = read_lines(args.input, cast=parse_line)

    print("Part 1:", part_1(boxes, connections=args.connections))
    print("Part 2:", part_2(boxes))


def parse_line(line: str) -> tuple[int, int, int]:
    x, y, z = map(int, line.split(","))
    return x, y, z


def get_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2


def part_1(boxes: list[tuple[int, int, int]], *, connections: int) -> int:
    pairs: list[int, int, int] = []

    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            box_1 = boxes[i]
            box_2 = boxes[j]

            distance = get_distance(box_1, box_2)
            pairs.append((distance, i, j))

    pairs.sort()

    circuits = [{i} for i in range(len(boxes))]

    for k in range(min(connections, len(pairs))):
        _, index_1, index_2 = pairs[k]

        circuit_1_index = None
        circuit_2_index = None

        for circuit_index, circuit in enumerate(circuits):
            if index_1 in circuit:
                circuit_1_index = circuit_index
            if index_2 in circuit:
                circuit_2_index = circuit_index

        if circuit_1_index != circuit_2_index:
            circuits[circuit_1_index].update(circuits[circuit_2_index])
            circuits.pop(circuit_2_index)

    sizes = [len(c) for c in circuits]
    sizes.sort(reverse=True)

    return sizes[0] * sizes[1] * sizes[2]


def part_2(boxes: list[tuple[int, int, int]]) -> int:
    pairs: list[int, int, int] = []

    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            box_1 = boxes[i]
            box_2 = boxes[j]

            distance = get_distance(box_1, box_2)
            pairs.append((distance, i, j))

    pairs.sort()

    parent = list(range(len(boxes)))
    circuits_left = len(boxes)
    last_pair = None

    def find(i: int) -> int:
        if parent[i] == i:
            return i
        parent[i] = find(parent[i])
        return parent[i]

    for distance, i, j in pairs:
        root_1 = find(i)
        root_2 = find(j)

        if root_1 != root_2:
            parent[root_1] = root_2
            circuits_left -= 1
            last_pair = (boxes[i], boxes[j])

        if circuits_left == 1:
            break

    return last_pair[0][0] * last_pair[1][0]


if __name__ == "__main__":
    main()
