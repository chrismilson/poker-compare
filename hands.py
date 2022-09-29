from collections import Counter
import unittest

# HELPER METHODS


def _card_suits(hand):
    cards = hand.split(" ")
    suits = map(lambda x: x[-1], cards)
    return list(suits)


def _card_numbers(hand):
    cards = hand.split(" ")
    numbers = map(lambda x: x[:-1], cards)
    return list(numbers)


def _k_n_tuples(hand, multiplicity, tuple_size):
    numbers = _card_numbers(hand)
    tuples = Counter(numbers)  # how many times each number appears
    n_tuples = Counter(tuples.values())  # how many times each tuple appears
    return n_tuples[tuple_size] == multiplicity


def _card_ordinals(hand):
    numbers = _card_numbers(hand)

    def number_to_ordinal(number):
        if number == 'A':
            return 1
        if number == 'K':
            return 13
        if number == 'Q':
            return 12
        if number == 'J':
            return 11
        return int(number)

    return list(map(number_to_ordinal, numbers))


def _difference(nums):
    it = iter(nums)

    try:
        prev = next(it)
    except StopIteration:
        return

    for num in it:
        yield num - prev
        prev = num


def _runs(nums):
    prev = 0
    count = 0
    for num in nums:
        if num == prev:
            count += 1
            continue

        if count > 0:
            yield count
        prev = num
        count = 1
    if count > 0:
        yield count


def _n_straight(hand, length):
    # in the range 1-13
    ordinals = _card_ordinals(hand)
    ordinals.sort()

    # translate to 0-12
    normal = max(_runs(_difference(map(lambda x: x - 1, ordinals))))

    # also translate to 12-24 (mod 13) to check for Ace high straight
    special = max(_runs(_difference(map(lambda x: (x + 11) % 13, ordinals))))

    return normal >= length or special >= length


def _n_flush(hand, length):
    suits = _card_suits(hand)
    tuples = Counter(suits)  # how many times each number appears
    n_tuples = Counter(tuples.values())  # how many times each tuple appears
    return n_tuples[length] == 1


class TestHelperMethods(unittest.TestCase):
    def test_runs(self):
        sequence = [1, 2, 3, 3, 3]
        # ONE one, ONE two, THREE threes
        expect = [1, 1, 3]

        self.assertListEqual(list(_runs(sequence)), expect)

# HANDS


def royal_flush(hand):
    ordinals = set(_card_ordinals(hand))
    return straight_flush(hand) and (1 in ordinals) and (13 in ordinals)


def four_of_a_kind(hand):
    return _k_n_tuples(hand, 1, 4)


def straight_flush(hand):
    return flush(hand) and straight(hand)


def full_house(hand):
    return _k_n_tuples(hand, 1, 3) and _k_n_tuples(hand, 1, 2)


def straight(hand):
    _n_straight(hand, 5)


def flush(hand):
    return _n_flush(hand, 5)


def three_of_a_kind(hand):
    return _k_n_tuples(hand, 1, 3)


def two_pair(hand):
    return _k_n_tuples(hand, 2, 2)


def one_pair(hand):
    return _k_n_tuples(hand, 1, 2)


class TestHandRanks(unittest.TestCase):
    def test_royal_flush(self):
        good = "AC KC JC QC 10C"
        bad = "AC 2C 3C 4C 5C"

        self.assertTrue(royal_flush(good))
        self.assertFalse(royal_flush(bad))

    def test_four_of_a_kind(self):
        good = "AC AH AD AS 10C"
        bad = "2C 2D 2H 3S 3C"

        self.assertTrue(four_of_a_kind(good))
        self.assertFalse(four_of_a_kind(bad))


if __name__ == "__main__":
    unittest.main()
