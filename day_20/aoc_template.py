# aoc_template.py

import pathlib
import sys
import re
from typing import Iterator
from functools import reduce
from collections import deque

def parse_line(
        line: str
        ) -> (str, tuple[str, list[str]]):
    module, dest = (x.strip() for x in re.split(r'->', line))

    if module == 'broadcaster':
        module_name = 'broadcaster'
        module_type = 'broadcaster'
    else:
        module_type, module_name = module[:1], module[1:]

    dest_list = [x.strip() for x in dest.split(',')]

    return (module_name, (module_type, dest_list))


def parse(
        puzzle_input: str
        ) -> dict[str, tuple[str, list[str]]]:
    """Parse input"""
    return dict (
        parse_line(line)
        for line
        in puzzle_input.split('\n')
    )


def get_inputs_for_conjunctions(
        data: dict[str, tuple[str, list[str]]]
        ) -> dict[str, list[str]]:
    
    dict_conjunctions = {
        key: []
        for key, val 
        in data.items()
        if val[0] == '&'
    }

    for key, value in data.items():
        for output in value[1]:
            if output in dict_conjunctions:
                dict_conjunctions[output] += [key]

    return dict_conjunctions


def init_state(
        data: dict[str, tuple[str, list[str]]],
        ) -> dict[str, str]:

    return {
        key:'low'
        for key
        in data.keys()
        if key != 'broadcaster' 
        }    


def send_pulse(
        data, 
        state, 
        conjunction_input_mapping, 
        pulse_val, 
        dest 
    ):
    state = state.copy()

def mk_push_button(
        data: dict[str, tuple[str, list[str]]],
        ) -> callable: 

    conjunction_input_mapping = get_inputs_for_conjunctions(data) 
    
    def push_button(
        state: dict[str, str]
        ) -> dict[str, str]:

        pulse_queue: deque
        pulse_queue = deque(
            (
                ('low', x)
                for x in data['broadcaster'][1]
            )
        )

        while len(pulse_queue) > 0:
            pulse_val, dest = pulse_queue.popleft()
            
            state, new_pulses = send_pulse(
                data, state, conjunction_input_mapping, pulse_val, dest 
            )

            pulse_queue.extend(new_pulses)


    return push_button



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
