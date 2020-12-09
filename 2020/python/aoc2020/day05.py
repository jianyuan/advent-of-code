from pydantic import BaseModel, constr

from .utils import read_lines_from_file


class Seat(BaseModel):
    space_id: constr(regex=r"^[FB]{7}[LR]{3}$")

    @classmethod
    def from_line(cls, line):
        return cls(space_id=line)

    @property
    def seat_id(self):
        mapping = {"F": "0", "B": "1", "L": "0", "R": "1"}
        return int("".join(map(mapping.__getitem__, self.space_id)), base=2)


if __name__ == "__main__":
    example_1 = Seat(space_id="BFFFBBFRRR")
    assert example_1.seat_id == 567

    example_2 = Seat(space_id="FFFBBBFRRR")
    assert example_2.seat_id == 119

    example_3 = Seat(space_id="BBFFBBFRLL")
    assert example_3.seat_id == 820

    seats = read_lines_from_file("day05.txt", cast=Seat.from_line)
    seat_ids = [seat.seat_id for seat in seats]

    print(max(seat_ids))

    print(
        next(
            seat_id
            for seat_id in range(min(seat_ids), max(seat_ids))
            if seat_id not in seat_ids
        )
    )
