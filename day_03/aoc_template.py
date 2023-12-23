# aoc_template.py

import pathlib
import sys
import re
from typing import Iterator
from itertools import combinations


def parse(puzzle_input: str) -> list[list[str]]:
    """Parse input"""
    return [
        list(x.strip()) for x in puzzle_input.split('\n')
    ]


def get_all_numbers(
        data: list[list[str]]
        ) -> list[tuple[int, int, tuple[int, int]]]:
    return [ 
        number_data
        for line_number, line in enumerate(data)
        for number_data
        in (
             (int(match.group(0)),line_number,(match.start(), match.end()-1))
             for match
             in re.finditer(r'(\d+)', ''.join(line))
           )
    ]


def get_all_symbols(
        data: list[list[str]]
        ) -> dict[tuple[int, int], str]:
    return {
        (line_number, column_number): symbol
        for line_number, line in enumerate(data)
        for column_number, symbol
        in enumerate(line)
        if not symbol.isnumeric() and symbol != '.'
    } 

def number_is_adjacent_to_symbol(
    number_data: tuple[int, int, tuple[int, int]],
    symbol_data: tuple[int, int]
    ) -> bool:
    n_y = number_data[1]
    n_start = number_data[2][0]
    n_end = number_data[2][1]
    s_y = symbol_data[0]
    s_x = symbol_data[1]

    return (
        s_x >= n_start - 1 and 
        s_x <= n_end + 1 and 
        s_y >= n_y - 1 and 
        s_y <= n_y + 1 
    )
    

def get_all_gears(
        data: list[list[str]]) -> dict[tuple[int, int], str]:
    return {
        x:y
        for x, y 
        in get_all_symbols(data).items()
        if y == '*'
    }

def numbers_share_gear(
        number_data_1: tuple[int, int, tuple[int, int]],
        number_data_2: tuple[int, int, tuple[int, int]],
        set_of_gears: dict[tuple[int, int], str]) -> bool:
    
    return len(
        set( x 
             for x 
             in set_of_gears.keys() 
             if number_is_adjacent_to_symbol(number_data_1, x)
            ) &
        set( x 
             for x
             in set_of_gears.keys() 
             if number_is_adjacent_to_symbol(number_data_2, x)
            ) 
        ) > 0

def part1(data: list[list[str]]) -> int:
    """Solve part 1"""
    symbol_set = get_all_symbols(data)
    return sum(
        number_data[0]
        for number_data
        in get_all_numbers(data)
        if any(
            number_is_adjacent_to_symbol(number_data, symbol_data) 
            for symbol_data 
            in symbol_set.keys()
            )
        )


def part2(data: list[list[str]]) -> int:
    """Solve part 2"""
    set_of_gears = get_all_gears(data)
    return sum(
        number_data_1[0]*number_data_2[0]
        for number_data_1, number_data_2
        in combinations(get_all_numbers(data), 2)
        if (
            abs(number_data_1[1] - number_data_2[1]) <= 2 and
            numbers_share_gear(
                number_data_1,
                number_data_2,
                set_of_gears
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
