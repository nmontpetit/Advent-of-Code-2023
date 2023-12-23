# aoc_template.py

import pathlib
import sys
import re
from typing import Iterator
from functools import reduce


def parse(puzzle_input: str) -> list[str]:
    """Parse input"""
    return puzzle_input.strip().split(',')

def character_fcn(current_val:int, character:str) -> int:
    return 17*(current_val + ord(character)) % 256

def compute_hash(value:str) -> int:
    return reduce(
        character_fcn,
        value,
        0)

def part1(data: list[str]):
    """Solve part 1"""
    return sum(
       compute_hash(val) 
       for val in data
    )

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
