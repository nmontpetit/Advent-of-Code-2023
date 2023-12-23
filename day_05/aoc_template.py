# aoc_template.py

import pathlib
import sys
import re
from typing import Iterator, Optional
from more_itertools import first, grouper
from itertools import dropwhile, count
from functools import reduce

def parse_map_data(
        map_data_lines: str) -> tuple[
                                    tuple[str, str],
                                    list[tuple[int, int, int]]
                                    ]:
    map_desc, range_data = map_data_lines.split('\n', maxsplit=1) 
    return (
        tuple((x.strip() for x in re.split('-to-', map_desc.split(' ')[0]))), 
        [tuple(int(x) for x in mapping_range.split(' '))
         for mapping_range in range_data.split('\n')
         ]
    )

def parse(puzzle_input: str) -> tuple[list[int], 
                                      list[
                                          tuple[
                                            tuple[str, str], 
                                            list[tuple[int, int, int]]
                                            ]
                                        ]
                                    ]:
    """Parse input"""
    seed_data, mapping_data = puzzle_input.split('\n\n', maxsplit=1)
    seed_list = [int(x) for x in re.findall(r'\d+', seed_data)]

    map_data_list = [
        parse_map_data(map_data_lines)
        for map_data_lines 
        in re.split(r'\n\n', mapping_data.strip())
        ]

    return (seed_list, map_data_list)


def apply_range(
        range_list: tuple[int, int, int], 
        value: int) -> Optional[int]:
    dest_start, source_start, length = range_list
    if value >= source_start and value < source_start + length:
        return dest_start + value - source_start
    else:
        return None


def apply_range_to_get_source(
        range_list: tuple[int, int, int], 
        value: int) -> Optional[int]:
    dest_start, source_start, length = range_list
    if value >= dest_start and value < dest_start + length:
        return source_start + value - dest_start
    else:
        return None


def mk_map_fcn(
        map_data: list[tuple[int, int, int]],
        apply_range_fcn = apply_range
    ):

    def apply_map(val):
        mapped_value = first(
            dropwhile(
                lambda x: x is None,
                ( apply_range_fcn(range_list, val) 
                  for range_list in map_data
                )
            ), None
        )
        return val if mapped_value is None else mapped_value

    return apply_map

def map_map_fcns(
    map_data: list[
                tuple[
                    tuple[str, str], 
                    list[tuple[int, int, int]]
                ]
              ]):
    return [
        (map_desc, mk_map_fcn(map_data))
        for map_desc, map_data
        in map_data
    ]

def map_map_fcns_reverse(
    map_data: list[
                tuple[
                    tuple[str, str], 
                    list[tuple[int, int, int]]
                ]
              ]):
    return [
        (map_desc, mk_map_fcn(map_data, apply_range_fcn=apply_range_to_get_source))
        for map_desc, map_data
        in reversed(map_data)
    ]

def apply_all_maps(all_maps, val):
    return reduce(lambda res, f: f(res), (x[1] for x in all_maps), val)


def mk_seed_generator(seed_list: tuple[int]):
    return (
        value
        for start, length in grouper(seed_list, 2)
        for value in range(start, start+length)
    )

def mk_seed_test(seed_list: tuple[int]):
    def seed_test(val):
        return any(
            start <= val < start + length
            for start, length in grouper(seed_list, 2)
        )
    return seed_test
    

def part1(data: tuple[list[int], 
                      list[
                        tuple[
                            tuple[str, str], 
                            list[tuple[int, int, int]]
                            ]
                        ]
                     ]) -> int:
    """Solve part 1"""
    all_maps = map_map_fcns(data[1])

    return min(apply_all_maps(all_maps, x) for x in data[0])

def part2(data: tuple[list[int], 
                      list[
                        tuple[
                            tuple[str, str], 
                            list[tuple[int, int, int]]
                            ]
                        ]
                     ]) -> int:
    """Solve part 2"""
    all_maps = map_map_fcns_reverse(data[1])
    in_seeds = mk_seed_test(data[0])

    mapped_value = first(
            dropwhile(
                lambda x: not in_seeds(x[1]),
                ( (val, apply_all_maps(all_maps, val))
                  for val in count(0)
                )
            ), None
        )

    return mapped_value[0]


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
