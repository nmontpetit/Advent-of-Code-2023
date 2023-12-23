# aoc_template.py

import pathlib
import sys
import re
from typing import Iterator


def parse(puzzle_input: str) -> dict[(int, int), int]:
    """Parse input"""
    return {
        (x, y):int(val)
        for y, line in enumerate(puzzle_input.split('\n'))
        for x, val in enumerate(line)
    }


def mk_point_iterator(data: dict[(int, int), int], history


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
