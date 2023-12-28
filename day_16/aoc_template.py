# aoc_template.py

import pathlib
import sys
from typing import Iterator
from itertools import accumulate, count, takewhile
from more_itertools import first


def parse(
        puzzle_input: str
        ) -> dict[tuple[int, int], str]:
    """Parse input"""
    return {
        (x, y): val
        for y, row in enumerate(puzzle_input.split('\n'))
        for x, val in enumerate(row)
        if val != '.'
    }


def update_point_by_one(
        point: tuple[tuple[int, int], str]
        ) -> tuple[tuple[int, int], str]:
    """Given a point and direction, return new point after moving one unit in
       the given direction.""" 
    (x, y), dir = point
    if   dir == 'L': return ((x-1, y), dir)
    elif dir == 'R': return ((x+1, y), dir)
    elif dir == 'U': return ((x, y-1), dir)
    else:            return ((x, y+1), dir)


def mk_lists_of_points_covered(
        data: dict[tuple[int, int], str],
        starting_point: tuple[tuple[int, int], str]
        ) -> list[list[tuple[tuple[int, int], str]]]:
    """There's got to be a better way."""

    max_x = max(x for x, _ in data.keys())
    max_y = max(y for _, y in data.keys())

    lists_to_try = [[starting_point]]
    points_covered_lists = []
    visited_points = set()

    while len(lists_to_try) > 0:
        points_covered_list = lists_to_try.pop(0)

        while True:
            next_point = update_point_by_one(points_covered_list[-1])
            x, y = next_point[0]
            if ( x > max_x or x < 0 or y < 0 or y > max_y or 
                 next_point in visited_points
               ):
                break               

            points_covered_list += [next_point]
            visited_points.add(next_point)

            if next_point[0] in data:
                reflector_type = data[next_point[0]]
                direction = next_point[1]

                if direction == 'R' and reflector_type == '\\':
                    points_covered_list += [(next_point[0], 'D')] 
                elif direction == 'R' and reflector_type == '/':
                    points_covered_list += [(next_point[0], 'U')] 
                elif direction == 'R' and reflector_type == '|':
                    lists_to_try += [(points_covered_list.copy() + [(next_point[0], 'D')])]
                    points_covered_list += [(next_point[0], 'U')] 
                
                elif direction == 'L' and reflector_type == '\\':
                    points_covered_list += [(next_point[0], 'U')] 
                elif direction == 'L' and reflector_type == '/':
                    points_covered_list += [(next_point[0], 'D')] 
                elif direction == 'L' and reflector_type == '|':
                    lists_to_try += [(points_covered_list.copy() + [(next_point[0], 'D')])]
                    points_covered_list += [(next_point[0], 'U')] 

                elif direction == 'U' and reflector_type == '\\':
                    points_covered_list += [(next_point[0], 'L')] 
                elif direction == 'U' and reflector_type == '/':
                    points_covered_list += [(next_point[0], 'R')] 
                elif direction == 'U' and reflector_type == '-':
                    lists_to_try += [(points_covered_list.copy() + [(next_point[0], 'L')])]
                    points_covered_list += [(next_point[0], 'R')] 

                elif direction == 'D' and reflector_type == '\\':
                    points_covered_list += [(next_point[0], 'R')] 
                elif direction == 'D' and reflector_type == '/':
                    points_covered_list += [(next_point[0], 'L')] 
                elif direction == 'D' and reflector_type == '-':
                    lists_to_try += [(points_covered_list.copy() + [(next_point[0], 'L')])]
                    points_covered_list += [(next_point[0], 'R')] 

        points_covered_lists += [points_covered_list]
    
    return points_covered_lists
            

def get_energized_count(
        data: dict[tuple[int, int], str],
        starting_point: tuple[tuple[int, int], str]
        ) -> int:
    return len(
        set(
            point[0]
            for list_points
            in mk_lists_of_points_covered(data, starting_point)
            for point in list_points
        )
        ) - 1


def get_starting_points(
        data: dict[tuple[int, int]]
        ) -> list[tuple[tuple[int, int], str]]:
    pass


def part1(data: dict[tuple[int, int], str]) -> int:
    """Solve part 1"""
    return get_energized_count(data, ((-1, 0), 'R'))


def part2(data: dict[tuple[int, int], str]) -> int:
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