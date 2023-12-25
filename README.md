# Nick's 2023 Advent of Code Solutions
## Description
From the Advent of Code website:
> Advent of Code is an Advent calendar of small programming puzzles for a 
> variety of skill sets and skill levels that can be solved in any programming
> language you like.
- Website: www.adventofcode.com
- Language I'm using:  Python
### Repository Structure
- One folder for each day of the code challenge 
- Within each folder:
    - `aoc_template.py`: the module that contains the code for parsing the puzzle data and solving the puzzle
    - `test_aoc_template.py`: tests
    - `example1.txt` (and occasionally additional data data files): the example data provided for each day's puzzle
## Principles
### General Principles
**AI is not used in any form or fashion** 
What fun would it be to have ChatGPT do my work here?  All of these problems are solvable without the help of AI.

**I will not look up specific solutions to these problems.**

## Programming Principles
These are constraints I've put on myself when solving the Advent of Code problems. 
This is not an endorsement of any coding style or approach; it's just a reflection of my preferences for this project.
### Use Functional Programming Techniques as Much as Possible
- Avoid usage of `for` loops in favor of iterators and generator expresssions.
- Heavy usage of `itertools` and `more-itertools` modules.
### Use Only Standard Library Modules
- The one exception is my heavy usage of `more-itertools`, which I wish were part of the standard library.

## Apologies
**I'm not writing many tests (even though I probably should).**

**I'm not adding docstrings to my code.**

## Areas of Focus this Year
Every year I choose areas of focus for improvement.
- Type Hinting
- Using `functools.reduce` and `itertools.accumulate` instead of generator functions whenever possible. 
