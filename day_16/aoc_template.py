# aoc_template.py

import pathlib
import sys
from typing import Iterator
from itertools import dropwhile, accumulate, count
from more_itertools import first


def parse(
        puzzle_input: str
        ) -> dict[(int, int), str]:
    """Parse input"""
    return {
        (x, y): val
        for y, row in enumerate(puzzle_input.split('\n'))
        for x, val in enumerate(row)
        if val != '.'
    }

def mk_point_in_motion_ck(
        data: dict[(int, int), str],
        ) -> callable:
    def point_in_motion(
            point: tuple[tuple[int, int], str]
            ) -> bool:

        x, y = point[0]
        dir = point[1]
        max_x = max(x for x, _ in data.keys())
        max_y = max(y for _, y in data.keys())

        return (
            point[0] not in data and (
                (dir == 'R' and x < max_x) or
                (dir == 'L' and x > 0) or
                (dir == 'U' and y > 0) or
                (dir == 'D' and y < max_y)
            )
        )
    return point_in_motion


def update_point_by_one(
        point: tuple[tuple[int, int], str]
        ) -> tuple[tuple[int, int], str]:
    (x, y), dir = point
    if   dir == 'L': return ((x-1, y), dir)
    elif dir == 'R': return ((x+1, y), dir)
    elif dir == 'U': return ((x, y-1), dir)
    else:            return ((x, y+1), dir)


def update_iterator(
        point: tuple[tuple[int, int], str]
    ):
    return accumulate(
            count(),
            lambda x, _: update_point_by_one(x),
            initial = point
    )  


def advance_light(
        data: dict[(int, int), str],
        point: tuple[tuple[int, int], str]
        ) -> list[tuple[tuple[int, int], str]]:

    new_point = first(
        dropwhile(
            mk_point_in_motion_ck(data),
            update_iterator(point)
            )
        )

    return new_point


def mk_line_iterator(
        data: dict[(int, int), str],
        starting_point: tuple[tuple[int, int], str]
        ):
    return 



def part1(data):
    """Solve part 1"""
    pass

def part2(data):
    """Solve part 2"""
    pass


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)
    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = pathlib.Path(path).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
