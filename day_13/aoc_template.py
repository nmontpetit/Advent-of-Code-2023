# aoc_template.py

import pathlib
import sys
import re
from typing import Iterator


def parse(puzzle_input: str) -> list[list[list[str]]]:
    """Parse input"""
    return [ 
         [list(line) for line in pattern.strip().split('\n')]
         for pattern in re.split(r'\n\n', puzzle_input)
        ]


def transpose(pattern: list[list[str]]) -> list[list[str]]:
    return [
        [pattern[y][x] for y in range(len(pattern))]
        for x in range(len(pattern[0]))
    ]


def find_reflection_line(pattern: list[list[str]]) -> int:
    pattern_length = len(pattern)
    for row_num in range(1, pattern_length):
        length_1, length_2 = row_num, pattern_length - row_num
        min_pattern_length = min(length_1, length_2)
        sub_pattern_1, sub_pattern_2 = (
            pattern[:row_num][::-1][:min_pattern_length], 
            pattern[row_num:][:min_pattern_length]
        )

        if all(
            [ val_1 == val_2
              for line_1, line_2 in zip(sub_pattern_1, sub_pattern_2)
              for val_1, val_2 in zip(line_1, line_2)
            ]
        ): return row_num

    return None
        

def find_reflection_line_p2(pattern: list[list[str]]) -> int:
    pattern_length = len(pattern)
    for row_num in range(1, pattern_length):
        length_1, length_2 = row_num, pattern_length - row_num
        min_pattern_length = min(length_1, length_2)
        sub_pattern_1, sub_pattern_2 = (
            pattern[:row_num][::-1][:min_pattern_length], 
            pattern[row_num:][:min_pattern_length]
        )

        if sum(
            [ val_1 != val_2
              for line_1, line_2 in zip(sub_pattern_1, sub_pattern_2)
              for val_1, val_2 in zip(line_1, line_2)
            ]
        ) == 1: return row_num

    return None
        

def get_summary_value_for_pattern(pattern: list[list[str]]) -> int:
    value = find_reflection_line(pattern)
    if value is not None:
        return 100*value
    value = find_reflection_line(transpose(pattern))
    return value

def get_summary_value_for_pattern_p2(pattern: list[list[str]]) -> int:
    value = find_reflection_line_p2(pattern)
    if value is not None:
        return 100*value
    value = find_reflection_line_p2(transpose(pattern))
    return value

def part1(data: list[list[list[str]]]):
    """Solve part 1"""
    return sum(get_summary_value_for_pattern(pattern) for pattern in data)

def part2(data):
    """Solve part 2"""
    return sum(get_summary_value_for_pattern_p2(pattern) for pattern in data)


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
