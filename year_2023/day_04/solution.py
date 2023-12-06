import os
import re
from collections import defaultdict
from dataclasses import dataclass
from utils.io import write_output


@dataclass
class Card:
    id: int
    winning_numbers: set[int]
    my_numbers: set[int]

    def my_winning_numbers(self):
        return len(self.winning_numbers.intersection(self.my_numbers))


def read_input():
    cards = []
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for id, line in enumerate(file, 1):
            winning, numbers = line.strip().split(":")[1].split("|")
            winning_n = set(int(x.group(1)) for x in re.finditer(r"(\d+)", winning))
            my_numbers = set(int(x.group(1)) for x in re.finditer(r"(\d+)", numbers))
            cards.append(Card(id, winning_n, my_numbers))
    return cards


def solve_1(input):
    points = defaultdict(lambda: 0)
    for card in input:
        my_winning_numbers = card.my_winning_numbers()
        if my_winning_numbers == 1:
            points[card.id] = 1
        elif my_winning_numbers > 1:
            points[card.id] = pow(2, my_winning_numbers - 1)
    return sum(x for x in points.values())


def solve_2(input):
    occurrences = defaultdict(lambda: 1)
    for card in input:
        card_occurrences = occurrences[card.id]
        for i in range(card.id + 1, card.id + 1 + card.my_winning_numbers()):
            occurrences[i] += card_occurrences
    return sum(x for x in occurrences.values())


input = read_input()
write_output(solve_1(input), solve_2(input))
