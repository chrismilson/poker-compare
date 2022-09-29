# A card is denoted by a string like AC or 10H
# A five card hand is denoted by a space separated string of five cards like
# AH KH QH JH 10H

# https://en.wikipedia.org/wiki/List_of_poker_hands
# There are differen possible hands - we first need to determine the highest
# rank that applies to the hand
from hands import four_of_a_kind, straight_flush, full_house, flush, straight, \
    three_of_a_kind, two_pair, one_pair

hand_order = [
    # royal_flush,
    four_of_a_kind,
    straight_flush,
    full_house,
    flush,
    straight,
    three_of_a_kind,
    two_pair,
    one_pair
]
