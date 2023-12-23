# aoc_template.py

import pathlib
import sys
from typing import Iterator
from more_itertools import grouper, pairwise
from itertools import combinations
from more_itertools import interleave_longest


def parse(
        puzzle_input: str
        ) -> list[tuple[list[str], list[int]]]:
    """Parse input"""
    return [
        (list(x), [int(x.strip()) for x in y.split(',')])
        for x, y in
        grouper(
           ( val 
             for line
             in puzzle_input.split('\n')
             for val in line.split(' ')
           ), 
           2
        )
    ]

def iterate_potential_solutions(
        diagram: list[str],
        damaged_groups: list[int]
    ):
    count_total = len(diagram)
    count_bad = sum(damaged_groups)
    count_good = count_total - count_bad
    count_bad_groups = len(damaged_groups)
    count_good_groups = count_bad_groups + 1

    '''
    print(f'{count_total=}')
    print(f'{count_bad=}')
    print(f'{count_good=}')
    print(f'{count_bad_groups=}')
    print(f'{count_good_groups=}')
    '''

    if count_good == count_bad_groups - 1:
        return [
            [''] + ['']*(count_bad_groups - 1) + ['']
        ]

    count_goods_to_partition = count_good - (count_bad_groups - 1)
    count_all_to_partition = count_goods_to_partition + count_good_groups - 1
    partition_list = list(range(1, count_all_to_partition+1))

    '''
    print(f'{count_goods_to_partition=}')
    print(f'{count_all_to_partition=}')
    print(f'{partition_list=}')
    '''

    return [
        ['.'*(y-x-1)
         for x, y
         in pairwise([0] + list(combination) + [count_all_to_partition + 1])
        ]
        for combination
        in combinations(partition_list, count_good_groups-1)
    ]

def construct_string(
        list_good: list[str],
        list_bad_counts: list[int]
        ) -> str:
    return list_good[0] + ''.join(interleave_longest(
        ['#'*x for x in list_bad_counts],
        [x+'.' for x in list_good[1:-1]])
    ) + list_good[-1]
        
def create_all_strings(
        diagram: list[str],
        damaged_groups: list[int]
    ):
    solution_iterator = iterate_potential_solutions(diagram, damaged_groups)
    return [
        construct_string(list_good, damaged_groups)
        for list_good in solution_iterator
    ]

def compare_strings(
        diagram:str, 
        potential_solution:str
        ) -> bool:

    return all(x == '?' or x == y
               for x, y
               in zip(diagram, potential_solution)
              )

def (data: list[tuple[list[str], list[int]]]):

def part1(data: list[tuple[list[str], list[int]]]):
    """Solve part 1"""
    return sum(
            sum(compare_strings(row[0], x)
                for x
                in create_all_strings(row[0], row[1])
               )
            for row in data
    )

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
