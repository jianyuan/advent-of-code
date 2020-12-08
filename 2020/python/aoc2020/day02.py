import re
from typing import ClassVar

from pydantic import BaseModel

from .utils import read_lines_from_file


class PasswordPolicy(BaseModel):
    lo: int
    hi: int
    letter: str
    password: str

    pattern: ClassVar[re.Pattern] = re.compile(
        r"(?P<lo>\d+)-(?P<hi>\d+) (?P<letter>\w): (?P<password>\w+)"
    )

    @classmethod
    def from_line(cls, line):
        return cls(**cls.pattern.match(line).groupdict())

    @property
    def is_valid_part_1(self):
        return self.lo <= self.password.count(self.letter) <= self.hi

    @property
    def is_valid_part_2(self):
        lo_matched = self.password[self.lo - 1] == self.letter
        hi_matched = self.password[self.hi - 1] == self.letter
        return lo_matched != hi_matched


if __name__ == "__main__":
    examples = [
        PasswordPolicy.from_line(line)
        for line in [
            "1-3 a: abcde",
            "1-3 b: cdefg",
            "2-9 c: ccccccccc",
        ]
    ]
    print(sum(1 for password in examples if password.is_valid_part_1))
    print(sum(1 for password in examples if password.is_valid_part_2))

    passwords = list(read_lines_from_file("day02.txt", cast=PasswordPolicy.from_line))
    print(sum(1 for password in passwords if password.is_valid_part_1))
    print(sum(1 for password in passwords if password.is_valid_part_2))
