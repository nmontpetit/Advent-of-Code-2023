# aoc_template.py

import pathlib
import sys
import re
from typing import Iterator
from itertools import cycle, accumulate, count
from more_itertools import first
from functools import reduce
from math import lcm


def parse_node_spec(node_spec: str) -> tuple[str, tuple[str, str]]:
    node, l, r = re.findall(r'\w{3}', node_spec)
    return (node, (l, r))


def parse(
        puzzle_input: str
        ) -> tuple[list[str],
                   dict[str, tuple[str, str]]
                   ]:
    """Parse input"""
    lr_instructions_str, node_data = re.split(r'\n\n', puzzle_input)
    return (
        list(lr_instructions_str),
        dict (
            parse_node_spec(node_spec)
            for node_spec in node_data.split('\n')
        )
    )


def mk_node_iterator(
        data: tuple[list[str],
                   dict[str, tuple[str, str]]
                   ],
        starting_node='AAA'):
    lr_instructions, node_data = data
    return accumulate(
                zip(count(1), cycle(lr_instructions)),
                lambda x, y: ( node_data[x[0]][0] if y[1] == 'L' else node_data[x[0]][1],
                               y ),
                initial=(starting_node, (0, ''))
            )


def mk_z_node_iterator(
        data: tuple[list[str],
                   dict[str, tuple[str, str]]
                   ],
        starting_node='AAA'):
    lr_instructions, node_data = data
    return (x[1][0]
            for x in accumulate(
                zip(count(1), cycle(lr_instructions)),
                lambda x, y: ( node_data[x[0]][0] if y[1] == 'L' else node_data[x[0]][1],
                               y ),
                initial=(starting_node, (0, ''))
            )
            if x[0].endswith('Z')
    )


def get_final_step(node_iterator, dest_node='ZZZ'):
    return first(
        x for x in node_iterator
        if x[0] == dest_node
    )


def part1(
        data: tuple[list[str],
                   dict[str, tuple[str, str]]
                   ]
    ) -> int:
    return get_final_step(mk_node_iterator(data))[1][0]


def part2(
        data: tuple[list[str],
                   dict[str, tuple[str, str]]
                   ]
    ) -> int:
    return lcm(*[ next(z_iterator)
                  for z_iterator
                  in ( mk_z_node_iterator(data, x)
                       for x
                       in data[1]
                       if x.endswith('A')
                     )
                ]
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
