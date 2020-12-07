from pathlib import Path


def read_lines_from_file(filename, *, cast=None):
    p = Path(__file__).parent / filename
    with p.open() as f:
        for line in f:
            if cast is None:
                yield line
            else:
                yield cast(line)
