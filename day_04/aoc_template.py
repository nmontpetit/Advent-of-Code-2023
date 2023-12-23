# aoc_template.py

import pathlib
import sys
import re
from typing import Iterator
from functools import reduce

def process_line(line: str) -> list[int, list[int], list[int]]:
    card_data, number_data = line.split(':')
    return [
        int(re.search('\d+', card_data).group())
        ] + [ [ int(x) for x in re.split(r'\s+', number_list.strip())]
              for number_list
              in number_data.split('|')
            ]
    

def parse(puzzle_input: str) -> list[list[int, list[int], list[int]]]:
    """Parse input"""
    return [
        process_line(line)
        for line in puzzle_input.split('\n')
    ]

def get_points_for_match_count(match_count: int) -> int:
    return 0 if match_count == 0 else 2**(match_count - 1)


def update_counts_dict(
        counts_dict: dict[int, int],
        card_data: list[int, list[int], list[int]]
    ) -> dict[int, int]:
    card_number, winning_numbers, my_numbers = card_data
    winning_count = len(set(winning_numbers) & set(my_numbers))
    if winning_count == 0:
        return counts_dict
    for i in range(card_number + 1, card_number + winning_count + 1):
        if i in counts_dict:
            counts_dict[i] = counts_dict[i] + counts_dict[card_number]

    return counts_dict
    

def part1(data: list[list[int, list[int], list[int]]]):
    """Solve part 1"""
    return sum(
        get_points_for_match_count(
            len(set(winning_numbers) & set(my_numbers))
            )
        for _, winning_numbers, my_numbers
        in data 
    )

def part2(data: list[list[int, list[int], list[int]]]):
    """Solve part 2"""
    initial_card_counts = {
        int(i):1
        for i, _, _
        in data
    }

    final_dict_card_counts = reduce(
        update_counts_dict,
        data,
        initial_card_counts
    )

    return sum(final_dict_card_counts.values())


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
