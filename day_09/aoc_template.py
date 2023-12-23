# aoc_template.py

import pathlib
import sys
import re
from typing import Iterator
from more_itertools import pairwise
from itertools import takewhile
from functools import reduce


def parse(puzzle_input: str) -> list[list[int]]:
    """Parse input"""
    return [
        [int(x.strip()) for x in line.strip().split()]
        for line
        in puzzle_input.strip().split('\n')
    ]


def mk_accumulator(history: list[int]):
    while len(history) > 1:
        new_history = [x[1] - x[0] for x in pairwise(history)] 
        yield new_history
        history = new_history


def get_all_diffs(history: list[int]):
    return list(
        takewhile(
            lambda x: any(y != 0 for y in x),
            mk_accumulator(history)
        )
    )

def mk_predicted_value(history: list[int]):
    list_all_diffs = get_all_diffs(history)
    return reduce(
        lambda x, y: x + y[-1],
        [history] + list_all_diffs,
        0
    )

def mk_predicted_value_part_2(history: list[int]):
    list_all_diffs = get_all_diffs(history)
    return reduce(
        lambda x, y: y[0] - x,
        reversed([history] + list_all_diffs),
        0
    )

def part1(data: list[list[int]]):
    """Solve part 1"""
    return sum(mk_predicted_value(history) 
               for history 
               in data)

def part2(data):
    """Solve part 2"""
    return sum(mk_predicted_value_part_2(history) 
               for history 
               in data)


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
