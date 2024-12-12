from unittest import TestCase
from ddt import ddt, data, unpack

from index12 import get_price_of_fencing


# fencing_price = 140
INPUT1 = """AAAA
BBCD
BBCC
EEEC
"""

# fencing_price = 772
INPUT2 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""

# fencing_price = 1930
INPUT3 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""


@ddt
class TestIndex10(TestCase):
    @data(
        {'input': INPUT1, 'expected': 140},
        {'input': INPUT2, 'expected': 772},
        {'input': INPUT3, 'expected': 1930},
    )
    @unpack
    def test_get_sum_of_scores(self, input: str, expected: int):
        result = get_price_of_fencing(input)
        self.assertEqual(result, expected)
