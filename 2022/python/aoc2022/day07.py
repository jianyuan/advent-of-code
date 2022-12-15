from .utils import read_lines_from_file_iter


def get_data():
    def make_dir():
        return {"type": "dir", "size": 0, "contents": {}}

    def make_file(size: int):
        return {"type": "file", "size": size}

    dir_stack = []
    fs = make_dir()

    for line in read_lines_from_file_iter("day07.txt"):
        match line.split():
            case ["$", "cd", "/"]:
                dir_stack = [fs]
            case ["$", "cd", ".."]:
                dir_stack.pop()
            case ["$", "cd", d]:
                dir_stack.append(dir_stack[-1]["contents"][d])
            case ["$", "ls"]:
                pass
            case ["dir", d]:
                assert d not in dir_stack[-1]["contents"]
                dir_stack[-1]["contents"][d] = make_dir()
            case [size, f]:
                assert f not in dir_stack[-1]["contents"]
                dir_stack[-1]["contents"][f] = make_file(int(size))
                for d in dir_stack:
                    d["size"] += int(size)
            case _:
                raise NotImplementedError(line)
    return fs


def part_1():
    fs = get_data()

    result = 0
    stack = [fs]
    while stack:
        current = stack.pop()
        if current["type"] == "file":
            continue
        if current["size"] <= 100000:
            result += current["size"]
        stack.extend(current["contents"].values())

    return result


def part_2():
    fs = get_data()

    free = 70000000 - fs["size"]
    need = 30000000 - free

    result = fs["size"]
    stack = [fs]
    while stack:
        current = stack.pop()
        if current["type"] == "file":
            continue
        if current["size"] < need:
            continue
        result = min(result, current["size"])
        stack.extend(current["contents"].values())

    return result


def main():
    print("Part 1:", part_1())
    print("Part 2:", part_2())


if __name__ == "__main__":
    main()
