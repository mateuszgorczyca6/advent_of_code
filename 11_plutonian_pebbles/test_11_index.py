from unittest import TestCase
from ddt import ddt, data, unpack

from index11 import get_num_of_stones


# score = 1
INPUT = """125 17
"""


@ddt
class TestIndex10(TestCase):
    @data(
        {'blinks': 0, 'expected': 2},
        {'blinks': 1, 'expected': 3},
        {'blinks': 2, 'expected': 4},
        {'blinks': 3, 'expected': 5},
        {'blinks': 4, 'expected': 9},
        {'blinks': 5, 'expected': 13},
        {'blinks': 6, 'expected': 22},
        {'blinks': 25, 'expected': 55312},
    )
    @unpack
    def test_get_sum_of_scores(self, blinks: int, expected: int):
        result = get_num_of_stones(INPUT, blinks)
        self.assertEqual(result, expected)
