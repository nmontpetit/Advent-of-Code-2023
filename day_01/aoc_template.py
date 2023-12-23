# aoc_template.py

import pathlib
import sys
import re
from typing import Iterator


def parse(puzzle_input: str) -> list[str]:
    """Parse input"""
    return puzzle_input.split('\n')

mapping_text_to_value = {
    'one'   : '1',
    'two'   : '2',
    'three' : '3',
    'four'  : '4',
    'five'  : '5',
    'six'   : '6',
    'seven' : '7',
    'eight' : '8',
    'nine'  : '9',
}

list_digits_as_strings = [str(x) for x in range(1, 10)]

def get_number(line: str, first: bool = True) -> str:
    line = line if first else line[::-1]
    min_pos_val = min(
        ( (val, match.start())
          for val in list(mapping_text_to_value.keys()) + list_digits_as_strings
          if (match := re.search(val if first else val[::-1], line)) is not None
        ),
        key = lambda x: x[1]
    )
    return mapping_text_to_value.get(min_pos_val[0], min_pos_val[0])

def part1(data: list[str]) -> int:
    """Solve part 1"""
    return sum(
        int(re.search(r'\d', val).group() + re.search(r'\d', val[::-1]).group())
        for val in data
        )

def part2(data):
    """Solve part 2"""
    return sum(
        int(get_number(val) + get_number(val, first=False))
        for val in data
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
