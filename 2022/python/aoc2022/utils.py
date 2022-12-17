from pathlib import Path


def read_file(filename):
    p = Path(__file__).parent / "data" / filename
    return p.read_text()


def read_lines_from_file_iter(filename, *, cast=None, strip=True):
    p = Path(__file__).parent / "data" / filename
    with p.open() as f:
        for line in f:
            if strip:
                line = line.strip()
            if cast:
                line = cast(line)
            yield line


def read_lines_from_file(filename, *, cast=None, strip=True):
    return list(read_lines_from_file_iter(filename, cast=cast, strip=strip))
