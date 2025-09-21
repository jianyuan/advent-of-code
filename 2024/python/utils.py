import pathlib
from typing import Callable, Iterator, TypeVar

T = TypeVar("T")


def read_lines_iter(filename: str, *, cast: Callable[[str], T] = str) -> Iterator[T]:
    with pathlib.Path(filename).open() as f:
        for line in f:
            yield cast(line.strip())


def read_lines(filename: str, *, cast: Callable[[str], T] = str) -> list[T]:
    return list(read_lines_iter(filename, cast=cast))


def read_line(filename: str, *, cast: Callable[[str], T] = str) -> T:
    return next(read_lines_iter(filename, cast=cast))
