# aoc_template.py

import pathlib
import sys
from typing import Iterator
from more_itertools import grouper


def parse(
        puzzle_input: str
        ) -> list[ 
                tuple[
                    tuple[int, int, int], 
                    tuple[int, int, int] 
                ]]:
    """Parse input"""
    return [
        ( tuple(int(x.strip()) for x in val1.split(',')),
          tuple(int(x.strip()) for x in val2.split(',')) )
        for val1, val2
        in grouper(
            ( val
              for line
              in puzzle_input.split('\n')
              for val in line.split('~')
            ), 2
        )
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
