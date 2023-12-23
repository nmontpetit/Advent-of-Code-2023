# aoc_template.py

import pathlib
import sys
import re
from typing import Iterator
from more_itertools import last, split_after
from itertools import count


def parse(puzzle_input: str) -> dict[tuple[int, int], str]:
    """Parse input"""
    return {
        (x, y): val
        for y, row
        in enumerate(puzzle_input.split('\n'))
        for x, val in enumerate(row.strip())
    }


def get_starting_pos(data: dict[tuple[int, int], str]) -> tuple[int, int]:
    return next(
        (x, y)
        for (x, y), val
        in data.items()
        if val == 'S'
    )

pipe_motion_mapping = {
    '|': ((0, 1),  (0, -1)),
    '-': ((1, 0),  (-1, 0)),
    'L': ((0, -1), (1, 0)),
    'J': ((0, -1), (-1, 0)),
    '7': ((0, 1),  (-1, 0)),
    'F': ((0, 1),  (1, 0)),
}

list_dir = [(0, -1), (1, 0), (0, 1), (-1, 0)]
list_eligible_types_for_dir = [
    ('|', '7', 'F'),
    ('-', '7', 'J'),
    ('|', 'L', 'J'),
    ('-', 'L', 'F'),
]

def add_dir(
    pos: tuple[int, int], 
    dir: tuple[int, int]) -> tuple[int, int]:
    return tuple(sum(x) for x in zip(pos, dir))

def get_pos_connected_to_start(
        data:dict[tuple[int, int], str]
    ) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    starting_pos = get_starting_pos(data)
    return [
        (new_pos, dir)
        for dir, list_eligible_types
        in zip(list_dir, list_eligible_types_for_dir)
        if (
            (new_pos := add_dir(starting_pos, dir)) in data and
            data[new_pos] in list_eligible_types
        )
    ]

def get_starting_type(
        data:dict[tuple[int, int], str]
    ) -> str:
    (pos_1, dir_1), (pos_2, dir_2) = get_pos_connected_to_start(data)
    set_dir = set((dir_1, dir_2))
    if (0, 1) in set_dir: 
        if   (0, -1) in set_dir: return '|'
        elif (1, 0) in set_dir: return 'F'
        elif (-1, 0 ) in set_dir: return '7'
    elif (0, -1) in set_dir: 
        if   (1, 0) in set_dir: return 'L'
        elif (-1, 0) in set_dir: return 'J'
    elif (-1, 0) in set_dir: return '-'


def mk_pipe_iterator(
        data:dict[tuple[int, int], str],
        dir: tuple[int, int] = list_dir[0] 
        ):
    starting_pos = get_starting_pos(data)
    yield starting_pos
    new_pos = add_dir(starting_pos, dir) 

    if new_pos not in (data) or data[new_pos] == '.':
        return

    pos_visited = set((starting_pos,))

    pos = new_pos
    while pos != starting_pos:
        yield pos
        pipe_type = data[pos]
        if pipe_type == 'S':
            return

        pos_visited.add(pos)
        try:
            new_pos = next(
                next_pos
                for dir in pipe_motion_mapping[pipe_type]  
                if (next_pos := add_dir(pos, dir)) not in pos_visited
            )
        except:
            return
        if new_pos == starting_pos:
            yield new_pos

        pos = new_pos

def get_all_loop_points(data):
    starting_dir   = get_pos_connected_to_start(data)[0][1]
    starting_point = get_starting_pos(data)
    starting_type  = get_starting_type(data)
    dict_loop = {
        pos:data[pos] 
        for pos 
        in mk_pipe_iterator(data, dir=starting_dir)
    }
    dict_loop[starting_point] = starting_type
    return dict_loop

def split_to_number(split):
    if split[0] == '|':
        return 1
    elif split[0] == 'F':
        if split[-1] == '7':
            return 2
        else:
            return 1
    elif split[0] == 'L':
        if split[-1] == 'J':
            return 2
        else:
            return 1
    else:
        return 0

def mk_count_intersections(data):
    max_x = max(y[0] for y in data.keys())
    loop_points = get_all_loop_points(data)
    def count_intersections(point):
        return sum(split_to_number(split)
                   for split
                   in  split_after(
                        [ loop_points[(x, point[1])] 
                          for x in range(point[0] + 1, max_x + 1) 
                          if (x, point[1]) in loop_points ],
                        lambda val: val in ('.', '|', '7', 'J')
                    ))
    
    return count_intersections

def part1(data: dict[tuple[int, int], str]) -> int:
    """Solve part 1"""
    starting_dir = get_pos_connected_to_start(data)[0][1]
    last_val = last(zip(
                    count(0),
                    mk_pipe_iterator(data, starting_dir)
                    ))

    return int(last_val[0]/2 + 1)

def part2(data):
    """Solve part 2"""
    all_loop_points = get_all_loop_points(data)
    count_intersections = mk_count_intersections(data)
    return sum(
        1 
        for point in data.keys()
        if point not in all_loop_points and count_intersections(point) % 2 == 1
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
