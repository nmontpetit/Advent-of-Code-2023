# aoc_template.py

import pathlib
import sys
import re
from typing import Iterator
from itertools import combinations


def parse(puzzle_input: str) -> set[tuple[int, int]]:
    """Parse input"""
    return { 
        (x, y)
        for y, row in enumerate(puzzle_input.split('\n'))
        for x, val in enumerate(row.strip())
        if val == '#'
    }

def expand_universe(
        data: set[tuple[int, int]],
        factor:int = 2
        ) -> set[tuple[int, int]]:
    set_x = {x for x, _ in data}
    set_y = {y for _, y in data}
    return {
        ( x + (factor - 1)*(x - len(set([z for z in set_x if z < x]))),
          y + (factor - 1)*(y - len(set([z for z in set_y if z < y])))
        )
        for x, y
        in data
    }

def get_man_distance(
        p_1: tuple[int, int],
        p_2: tuple[int, int]
        ) -> int:
    return sum(abs(y - x) for x, y in zip(p_1, p_2))


def part1(data: set[tuple[int, int]]):
    """Solve part 1"""
    return sum(
        get_man_distance(p_1, p_2)
        for p_1, p_2
        in combinations(expand_universe(data), 2)
    )

def part2(data):
    """Solve part 2"""
    return sum(
        get_man_distance(p_1, p_2)
        for p_1, p_2
        in combinations(expand_universe(data, factor=1_000_000), 2)
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
