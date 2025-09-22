import argparse
from pprint import pprint

from utils import read_line

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="Path to input file")


def parse_disk_map(disk_map: list[str]) -> list[int | None]:
    storage: list[int | None] = []
    for i, c in enumerate(disk_map):
        if i % 2 == 0:
            for _ in range(int(c)):
                storage.append(i // 2)
        else:
            for _ in range(int(c)):
                storage.append(None)
    return storage


def calculate_checksum(storage: list[int | None]) -> int:
    return sum(i * int(data) for i, data in enumerate(storage) if data is not None)


def render_storage(storage: list[int | None]) -> str:
    return "".join("." if c is None else f"[{c}]" for c in storage)


def part_1(storage: list[int | None]) -> int:
    storage = storage[:]
    a, b = 0, len(storage) - 1
    while a < b:
        while storage[a] is not None and a < b:
            a += 1
        while storage[b] is None and a < b:
            b -= 1
        storage[a], storage[b] = storage[b], storage[a]
    return calculate_checksum(storage)


def part_2(storage: list[int | None]) -> int:
    storage = storage[:]
    print(render_storage(storage))

    data_b = len(storage) - 1
    last_data: int | None = None
    while data_b > 0:
        while storage[data_b] is None or (
            last_data is not None and storage[data_b] >= last_data
        ):
            data_b -= 1
        data_a = data_b
        while storage[data_a - 1] == storage[data_b]:
            data_a -= 1
        data_size = data_b - data_a + 1

        free_a = 0
        while free_a < data_a:
            while storage[free_a] is not None:
                free_a += 1
            free_b = free_a
            while free_b + 1 < len(storage) and storage[free_b + 1] is None:
                free_b += 1
            free_size = free_b - free_a + 1

            if free_size >= data_size:
                for i in range(data_size):
                    storage[data_a + i], storage[free_a + i] = (
                        storage[free_a + i],
                        storage[data_a + i],
                    )
                break
            else:
                free_a += free_size
        else:
            last_data = storage[data_b]
            data_b -= data_size

    return calculate_checksum(storage)


def xxx_part_2(storage: list[int | None]) -> int:
    storage = storage[:]
    free_a, data_b = 0, len(storage) - 1

    while storage[data_b] is None:
        data_b -= 1

    while free_a < data_b:
        print(f"START {free_a=} {data_b=}")
        print("BE:", render_storage(storage))
        while storage[free_a] is not None and free_a < data_b:
            free_a += 1
        free_b = free_a
        while storage[free_b + 1] is None:
            free_b += 1
        free_size = free_b - free_a + 1
        print(f"{free_a=} {free_b=} {free_size=}")

        next_data_b = data_b
        while free_b < next_data_b:
            while storage[next_data_b] is None:
                next_data_b -= 1

            next_data_a = next_data_b
            while storage[next_data_a - 1] == storage[next_data_b]:
                next_data_a -= 1
            next_data_size = next_data_b - next_data_a + 1
            print(f"{next_data_a=} {next_data_b=} {next_data_size=}")

            if next_data_size > 1 and free_size >= next_data_size:
                print("!!! BEFOR MOVE:", render_storage(storage))
                for i in range(next_data_size):
                    storage[next_data_a + i], storage[free_a + i] = (
                        storage[free_a + i],
                        storage[next_data_a + i],
                    )
                free_a += next_data_size
                data_b -= next_data_size
                print("!!! AFTER MOVE:", render_storage(storage))
                break
            else:
                next_data_b -= next_data_size + 1
        else:
            free_a += 1

    return calculate_checksum(storage)


def main():
    args = parser.parse_args()
    storage = parse_disk_map(list(read_line(args.input)))

    print("Part 1:", part_1(storage=storage))
    print("Part 2:", part_2(storage=storage))


if __name__ == "__main__":
    main()
