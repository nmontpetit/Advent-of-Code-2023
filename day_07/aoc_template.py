# aoc_template.py

import pathlib
import sys
import re
from typing import Iterator
from collections import Counter
from functools import cmp_to_key


def parse_line(line: str) -> tuple[
                                tuple[str, str, str, str, str],
                                int
                                ]:
    hand, bid = (x.strip() for x in re.split('\s', line))
    return (tuple(hand), int(bid))


def parse(puzzle_input: str) -> list[tuple[
                                        tuple[str, str, str, str, str], 
                                        int]
                                        ]:
    """Parse input"""
    return [
        parse_line(line)
        for line
        in puzzle_input.strip().split('\n')
    ]


card_rank_mapping = {
    x:i
    for i, x
    in enumerate(['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'])
    }

card_rank_mapping_part_2 = {
    x:i
    for i, x
    in enumerate(['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J'])
    }

def mk_count_of_counts(
    cards: tuple[str, str, str, str, str]
    )-> Counter:
    return Counter(Counter(cards).values())

def rank_hand(
    cards: tuple[str, str, str, str, str]
    ) -> int:
    count_of_counts = mk_count_of_counts(cards)

    if max(count_of_counts.keys()) == 5:
        return 0
    elif max(count_of_counts.keys()) == 4:
        return 1
    elif 3 in count_of_counts.keys() and 2 in count_of_counts.keys():
        return 2
    elif 3 in count_of_counts.keys():
        return 3
    elif 2 in count_of_counts.keys() and count_of_counts[2] == 2:
        return 4
    elif 2 in count_of_counts.keys():
        return 5
    else:
        return 6

    return count_of_counts.most_common(1)

def compare_first_diff(
        hand_1: tuple[str, str, str, str, str], 
        hand_2: tuple[str, str, str, str, str],
        card_rank_mapping = card_rank_mapping
        ) -> int:
    list_diff = [
        (x, y)
        for x, y
        in zip(hand_1, hand_2)
        if x != y
    ]

    if len(list_diff) == 0:
        return 0 

    first_diff = list_diff[0]

    return -1 if card_rank_mapping[first_diff[0]] > card_rank_mapping[first_diff[1]] else 1


def mk_hand_comparison(
        hand_1_data: tuple[tuple[str, str, str, str, str], int], 
        hand_2_data: tuple[tuple[str, str, str, str, str], int],
        card_rank_mapping=card_rank_mapping
    ) -> int:
    hand_1 = hand_1_data[0]
    hand_2 = hand_2_data[0]
    hand_1_rank = rank_hand(hand_1)
    hand_2_rank = rank_hand(hand_2)

    if hand_1_rank != hand_2_rank:
        return -1 if hand_1_rank > hand_2_rank else 1
    return compare_first_diff(hand_1, hand_2, card_rank_mapping)


def find_replacement_value(hand: tuple[str, str, str, str, str]):
    counter_not_jacks = Counter([x for x in hand if x != 'J'])
    
    max_count = max(counter_not_jacks.values())
    return min((x[0] for x in counter_not_jacks.items() if x[1] == max_count),
               key=lambda val: card_rank_mapping[val])

def mk_new_hand(
    hand: tuple[str, str, str, str, str]) -> tuple[str, str, str, str, str, str]:
    if hand == ('J', 'J', 'J', 'J', 'J'):
        return ('A', 'A', 'A', 'A', 'A')
    
    replacement_value = find_replacement_value(hand)
    
    return tuple(replacement_value if x == 'J' else x for x in hand)

def mk_hand_comparison_part_2(
        hand_1_data: tuple[tuple[str, str, str, str, str], int], 
        hand_2_data: tuple[tuple[str, str, str, str, str], int],
        card_rank_mapping=card_rank_mapping
    ) -> int:
    hand_1 = hand_1_data[0]
    hand_2 = hand_2_data[0]
    new_hand_1 = mk_new_hand(hand_1)
    new_hand_2 = mk_new_hand(hand_2)
    hand_1_rank = rank_hand(new_hand_1)
    hand_2_rank = rank_hand(new_hand_2)

    if hand_1_rank != hand_2_rank:
        return -1 if hand_1_rank > hand_2_rank else 1
    return compare_first_diff(hand_1, hand_2, card_rank_mapping_part_2)

def mk_new_list_of_hands(
        data: list[tuple[
                    tuple[str, str, str, str, str], 
                    int]
                  ])-> list[tuple[
                                tuple[str, str, str, str, str], 
                                int]
                           ]:
    return [ (mk_new_hand(hand), bid)
             for hand, bid
             in data
           ]

    
def part1(data):
    """Solve part 1"""
    return sum(
        i*hand_data[1]
        for i, hand_data
        in enumerate(
            sorted(data, key=cmp_to_key(mk_hand_comparison)),
            start=1
        )
    )

def part2(data):
    """Solve part 2"""
    new_list_of_hands = mk_new_list_of_hands(data)
    return sum(
        i*hand_data[1]
        for i, hand_data
        in enumerate(
            sorted(new_list_of_hands, key=cmp_to_key(mk_hand_comparison_part_2)),
            start=1
        )
    )

def part2(data):
    """Solve part 2"""
    return sum(
        i*hand_data[1]
        for i, hand_data
        in enumerate(
            sorted(data, key=cmp_to_key(mk_hand_comparison_part_2)),
            start=1
        )
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
