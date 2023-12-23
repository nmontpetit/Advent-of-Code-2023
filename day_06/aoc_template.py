# aoc_template.py

import pathlib
import sys
import re
from typing import Iterator
from math import sqrt, floor, ceil
from functools import reduce


def parse(puzzle_input: str) -> list[tuple[int, int]]:
    """Parse input"""
    return list(zip(
        *[[int(x) for x in re.findall(r'\d+', row)]
         for row 
         in puzzle_input.split('\n')
        ]
        ))

def calculate_roots(T:int, d:int) -> tuple[int, int]:
    sqrt_term = sqrt(T**2 - 4*d)
    roots = sorted([(T + sqrt_term)/2, (T - sqrt_term)/2])
    return (floor(roots[0]), ceil(roots[1]))

def get_count_from_roots(roots: tuple[int, int]):
    return roots[1] - roots[0] - 1

def part1(data: list[tuple[int, int]]) -> int:
    """Solve part 1"""
    return reduce(
        lambda x, y: x*y,
        (get_count_from_roots(calculate_roots(*line))
         for line in data
        )
    ) 

def part2(data: list[tuple[int, int]]) -> int:
    """Solve part 2"""
    return get_count_from_roots(
        calculate_roots(
            *tuple(
                int(x)
                for x
                in reduce(
                    lambda x, y: (x[0] + y[0], x[1] + y[1]),
                    ([str(x) for x in y] for y in data))
                )
        )
    )


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
