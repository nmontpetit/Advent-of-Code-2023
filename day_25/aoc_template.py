# aoc_template.py

import pathlib
import sys
import re
from typing import Iterator
from more_itertools import grouper 


def parse(
        puzzle_input: str
        ) -> list[tuple[str, str]]:
    """Parse input"""
    return [
        (x.strip(), y.strip()) if x < y else (y.strip(), x.strip())
        for x, component_list
        in grouper(
            ( val 
              for line in puzzle_input.split('\n')
              for val in line.split(':')
            ), 2)
       for y in component_list.split() 
    ]


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
