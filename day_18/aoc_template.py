# aoc_template.py

import pathlib
import sys
import re
from typing import Iterator
from more_itertools import grouper
from itertools import accumulate, repeat


def parse(
        puzzle_input: str
        ) -> list[tuple[str, int, str]]:
    """Parse input"""
    return [
        (direction, int(distance), re.search(r'\((#\w+)', color).groups()[0])
        for direction, distance, color
        in grouper(
            ( value
              for line in puzzle_input.split('\n')
              for value in line.split()
            ),
            3
        )
    ]

dir_mapping = {
    'U': ( 0, -1),
    'D': ( 0,  1),
    'L': (-1,  0),
    'R': ( 1,  0),
}

def advance_digger(
        pos: tuple[int, int], 
        dir: str) -> tuple[int, int]:
    return tuple((x+y for x, y in zip(pos, dir_mapping[dir])))

def mk_dig_path_iterator(
        data: list[tuple[str, int, str]]
        ):
    return (
        accumulate(
            ( single_dir 
              for (dir, dist, _)
              in data
              for single_dir
              in repeat(dir, dist)
            ),
            lambda x, y: advance_digger(x, y),
            initial = (0, 0)
        )
    )

def get_all_interior_points(
        data: list[tuple[str, int, str]],
        dig_path
        )

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
