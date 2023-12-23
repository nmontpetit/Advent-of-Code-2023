# aoc_template.py

import pathlib
import sys
import re
from typing import Iterator
from functools import reduce
from itertools import accumulate, count
from hashlib import sha256
from more_itertools import first

def parse(puzzle_input: str) -> dict[tuple[int, int], str]:
    """Parse input"""
    return {
        (x, y): val
        for y, line in enumerate(puzzle_input.split('\n'))
        for x, val in enumerate(line)
        if val in ('#', 'O')
    }


def adjust_column(
        data: dict[tuple[int, int], str], 
        col_num: int
        ) -> dict[tuple[int, int], str]:
    return reduce(
        lambda x, y: x + [y] if y[1] == '#' else x + [((y[0][0], 0 if x == [] else x[-1][0][1]+1), y[1])],
        sorted(
            [ (key, value)
              for key, value
              in data.items()
              if key[0] == col_num
            ],
            key = lambda item: item[0][1]
        ),
        []
    )


def adjust_platform(
        data: dict[tuple[int, int], str]
        ) -> dict[tuple[int, int], str]:
    return {
        key: val
        for col_num in range(max(key[0] for key in data.keys())+1)
        for key, val in adjust_column(data, col_num)
    }

def display_platform(
        data: dict[tuple[int, int], str]
    ) -> dict[tuple[int, int], str]:
    max_x = max(y[0] for y in data.keys())
    max_y = max(y[1] for y in data.keys())

    return '\n'.join(
            ( ''.join((data.get((x, y), '.') for x in range(max_x + 1))) 
              for y in range(max_y + 1)
            )
            )


def rotate_platform(
        data: dict[tuple[int, int], str],
        platform: dict[tuple[int, int], str]
        ) -> dict[tuple[int, int], str]:
    max_y = max(y[1] for y in data.keys())
    return {
        (max_y - key[1], key[0]): val
        for key, val
        in platform.items()
    }

def run_cycle(
        data: dict[tuple[int, int], str],
        platform: dict[tuple[int, int], str],
        ) -> dict[tuple[int, int], str]:
    #cycle order:  N, W, S, E

    new_platform = adjust_platform(platform)
    new_platform = adjust_platform(rotate_platform(data, new_platform))
    new_platform = adjust_platform(rotate_platform(data, new_platform))
    new_platform = adjust_platform(rotate_platform(data, new_platform))
    new_platform = rotate_platform(data, new_platform)

    return new_platform


def mk_cycle_iterator(data):
    return accumulate(
        count(1),
        lambda x, y: (y, run_cycle(data, x[1])), 
        initial = (0, data)
    ) 

def mk_repeating_list(data):
    cycle_iterator = mk_cycle_iterator(data)
    list_cycle_vals = []
    set_cycle_str_vals = set()
    cycle_val = next(cycle_iterator)
    cycle_str_val = display_platform(cycle_val[1])
    list_cycle_vals += [(cycle_str_val, cycle_val[1])]
    while cycle_str_val not in set_cycle_str_vals:
        set_cycle_str_vals.add(cycle_str_val)
        cycle_val = next(cycle_iterator)
        cycle_str_val = display_platform(cycle_val[1])
        list_cycle_vals += [(cycle_str_val, cycle_val[1])]

    first_repeat_index = first(
        x
        for x, val 
        in enumerate(list_cycle_vals) 
        if val[0] == list_cycle_vals[-1][0])

    return (first_repeat_index, list_cycle_vals[first_repeat_index:-1])
    

def part1(data: dict[tuple[int, int], str]) -> int:
    """Solve part 1"""
    adjusted_platform = adjust_platform(data)
    max_y = max(x[1] for x in adjusted_platform.keys())
    return sum(
        (max_y + 1 - row_num)*sum(1 for key, val in adjusted_platform.items() if key[1] == row_num and val == 'O')
        for row_num in range(0, max_y+1)
    )

def part2(data):
    """Solve part 2"""
    starter_len, repeating_list = mk_repeating_list(data)
    platform = repeating_list[(1_000_000_000 - starter_len) % len(repeating_list)][1]
    max_y = max(x[1] for x in platform.keys())
    return sum(
        (max_y + 1 - row_num)*sum(1 for key, val in platform.items() if key[1] == row_num and val == 'O')
        for row_num in range(0, max_y+1)
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
