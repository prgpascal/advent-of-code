from enum import Enum
import os
from collections import Counter
from dataclasses import dataclass
from utils.io import write_output

CARD_VALUES = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "J": 10,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
}
CARD_VALUES_WITH_JOKER = dict(CARD_VALUES)
CARD_VALUES_WITH_JOKER["J"] = 0


class HandType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


def compute_type(hand) -> HandType:
    c = Counter(hand).most_common()
    if c[0][1] == 5:
        return HandType.FIVE_OF_A_KIND
    elif c[0][1] == 4:
        return HandType.FOUR_OF_A_KIND
    elif c[0][1] == 3 and c[1][1] == 2:
        return HandType.FULL_HOUSE
    elif c[0][1] == 3:
        return HandType.THREE_OF_A_KIND
    elif c[0][1] == 2 and c[1][1] == 2:
        return HandType.TWO_PAIR
    elif c[0][1] == 2:
        return HandType.ONE_PAIR
    else:
        return HandType.HIGH_CARD


def compute_type_with_joker(hand) -> HandType:
    if "J" not in hand:
        return compute_type(hand)

    c = Counter(hand).most_common()
    if c[0][1] == 5:
        return HandType.FIVE_OF_A_KIND  # JJJJJ -> JJJJJ
    elif c[0][1] == 4:
        return HandType.FIVE_OF_A_KIND  # JJJJ2 | 2222J -> 22222
    elif c[0][1] == 3 and c[1][1] == 2:
        return HandType.FIVE_OF_A_KIND  # JJJ22 | 222JJ -> 22222
    elif c[0][1] == 3:
        return HandType.FOUR_OF_A_KIND  # JJJ32 | 3332J -> 33332
    elif c[0][1] == 2 and c[1][1] == 2:
        if c[0][0] == "J" or c[1][0] == "J":
            return HandType.FOUR_OF_A_KIND  # JJ332 | 33JJ2 -> 33332
        else:
            return HandType.FULL_HOUSE  # 3322J -> 33322
    elif c[0][1] == 2:
        return HandType.THREE_OF_A_KIND  # JJ321 | 33J21-> 33321
    else:
        return HandType.ONE_PAIR  # J4321 -> 44321


@dataclass
class CamelCardsHand:
    hand: str
    bid: int
    with_jokers: bool = False

    @property
    def type(self) -> HandType:
        if self.with_jokers:
            return compute_type_with_joker(self.hand)
        return compute_type(self.hand)

    def __lt__(self, other):
        if self.type.value == other.type.value:
            # compare card by card
            cards_deck = CARD_VALUES_WITH_JOKER if self.with_jokers else CARD_VALUES
            for s, o in zip(self.hand, other.hand):
                if cards_deck[s] != cards_deck[o]:
                    return cards_deck[s] < cards_deck[o]
        return self.type.value <= other.type.value


def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        input = []
        for line in file:
            hand, bid = line.strip().split(" ")
            input.append(CamelCardsHand(hand, int(bid)))
        return input


def solve(cards: list[CamelCardsHand]):
    cards.sort()
    return sum(rank * hand.bid for rank, hand in enumerate(cards, 1))


def solve_1(input):
    return solve(input)


def solve_2(input):
    for x in input:
        x.with_jokers = True
    return solve(input)


input = read_input()
write_output(solve_1(input), solve_2(input))
