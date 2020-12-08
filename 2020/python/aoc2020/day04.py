import re
from typing import ClassVar

from pydantic import BaseModel, constr, Field, ValidationError, validator

from .utils import read_lines_from_file


expected_fields = {
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
    "cid",
}
optional_fields = {"cid"}


def parse_passports(lines):
    current_passport = {}
    passports = []

    for line in lines:
        if line == "":
            passports.append(current_passport)
            current_passport = {}
        else:
            fields = line.split(" ")
            for field in fields:
                key, value = field.split(":", 2)
                current_passport[key] = value

    if current_passport:
        passports.append(current_passport)

    return passports


def is_valid_passport_part_1(passport):
    return set(passport.keys()) >= expected_fields - optional_fields


def is_valid_passport_part_2(passport):
    try:
        Passport(**passport)
    except ValidationError:
        return False
    else:
        return True


class Passport(BaseModel):
    byr: int = Field(ge=1920, le=2002)
    iyr: int = Field(ge=2010, le=2020)
    eyr: int = Field(ge=2020, le=2030)
    hgt: str
    hgt_regex: ClassVar = re.compile(r"(\d+)(cm|in)")
    hcl: constr(regex=r"^#[\da-f]{6}$")
    ecl: constr(regex=r"^(amb|blu|brn|gry|grn|hzl|oth)$")
    pid: constr(regex=r"^\d{9}$")

    @validator("hgt")
    def check_height(cls, v):
        r = cls.hgt_regex.match(v)
        assert r is not None
        number, measurement = r.groups()
        assert (measurement == "cm" and 150 <= int(number) <= 193) or (
            measurement == "in" and 59 <= int(number) <= 76
        )
        return v


if __name__ == "__main__":
    example1_passports = parse_passports(read_lines_from_file("day04_example1.txt"))
    example2_passports = parse_passports(read_lines_from_file("day04_example2.txt"))
    passports = parse_passports(read_lines_from_file("day04.txt"))

    print(
        sum(1 for passport in example1_passports if is_valid_passport_part_1(passport))
    )
    print(sum(1 for passport in passports if is_valid_passport_part_1(passport)))

    print(
        sum(1 for passport in example2_passports if is_valid_passport_part_2(passport))
    )
    print(sum(1 for passport in passports if is_valid_passport_part_2(passport)))
