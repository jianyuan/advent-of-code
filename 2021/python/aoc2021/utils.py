from pathlib import Path


def read_lines_from_file_iter(filename, *, cast=None):
    p = Path(__file__).parent.parent / "data" / filename
    with p.open() as f:
        for line in f:
            if cast is None:
                yield line.strip()
            else:
                yield cast(line.strip())


def read_lines_from_file(filename, *, cast=None):
    return list(read_lines_from_file_iter(filename, cast=cast))
