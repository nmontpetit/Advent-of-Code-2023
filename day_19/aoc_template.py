# aoc_template.py

import pathlib
import sys
import re
from typing import Iterator
from more_itertools import grouper, first
from itertools import accumulate, count

def parse_rule(
        rule: str
        ) -> tuple[str, int, str, str]:
    rule_logic, dest = rule.split(':')
    return tuple(
       [int(x) if x.isnumeric() else x 
        for x in re.match(r'(\w+)([<>])(\d+)', rule_logic).groups()
       ] + [dest])


def parse_rules_data(
        rules_data: str
        ) -> tuple[list[tuple[str, int, str, str], str]]:
    rules_logic, default_dest = rules_data.rstrip('}').rsplit(',', maxsplit=1)
    return (
        [parse_rule(rule) for rule in rules_logic.split(',')], 
        default_dest
    )

def parse_workflow(
        workflow_data: str
        ) -> dict[str, tuple[list[tuple[str, int, str, str], str]]]:
    return {
        name:parse_rules_data(rules_data)
        for name, rules_data
        in grouper(
            ( value
              for rule in workflow_data.split('\n')
              for value in rule.split('{')
            ), 2
        )
    }
    

def parse_ratings(
        ratings_data: str
        ) -> list[dict[str, int]]:
    return [
        { x: int(y.rstrip('}'))
          for x, y
          in grouper( 
            ( value
              for pair_data
              in rating.split(',')
              for value in pair_data.split('=')
            ), 2
        )
        }
        for rating
        in ratings_data.split('\n')
    ]


def parse(
        puzzle_input: str
        ) -> tuple[
                dict[str, tuple[list[tuple[str, str, int, str], str]]],
                list[dict[str, int]]
            ]:
    """Parse input"""
    workflow_data, ratings_data = (x.strip() 
                                   for x in puzzle_input.split('\n\n'))
    return (
        parse_workflow(workflow_data),
        parse_ratings(ratings_data)
    )

def apply_rule(part_data, rule_data):
    default_val = rule_data[1]
    return 
    

def run_part_through_rules(
    part_data,
    rules
    ):
    return accumulate(
        count(),
        lambda x, y: apply_rule(x, y)
        initial = 'in'
    )



def part1(data):
    """Solve part 1"""
    pass

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
