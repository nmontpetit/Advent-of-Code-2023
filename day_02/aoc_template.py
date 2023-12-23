# aoc_template.py

import pathlib
import sys
import re
from typing import Iterator
from functools import reduce

def parse_game(game_id_str: str, 
               game_data: str) -> tuple[int, list[dict[str, int]]]:
    return (
        int(re.search(r'\d+', game_id_str).group()),
        [ {y:int(x) for x, y in re.findall(r'(\d+)\s*(\w+)', draw_data)}
          for draw_data
          in game_data.split(';') 
        ] 
    )

def parse(puzzle_input: str) -> list[tuple[int, list[dict[str, int]]]]:
    """Parse input"""
    return [
        parse_game(*game.split(':'))
        for game in puzzle_input.split('\n')
    ]

game_question_data_part_1 = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

def game_is_possible(
        game_data: list[dict[str, int]], 
        game_question_data: dict[str, int] = game_question_data_part_1
        ) -> bool:
    return all(
        count <= game_question_data[color] 
        for draw_data in game_data
        for color, count in draw_data.items()
    )

def get_min_cubes_per_color(
        game_data: list[dict[str, int]]
    ) -> dict[str, int]:
    return reduce(
        lambda x, y: {
            key: x[key] if key not in y else y[key] if key not in x else max(x[key], y[key])
            for key in set(x.keys()) | set(y.keys())
            },
        game_data
    )


def part1(data):
    """Solve part 1"""
    return sum(
        game_id
        for (game_id, game_data)
        in data
        if game_is_possible(game_data)
    )

def part2(data):
    """Solve part 2"""
    return sum(
        reduce(
            lambda x, y: x*y,
            get_min_cubes_per_color(game_data).values()
        )
        for _, game_data
        in data
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
