from unittest import TestCase
from ddt import ddt, data, unpack

from index12 import get_price_of_fencing, get_price_of_fencing_with_discount, set_up


# fencing price = 140
# fencing price with discount = 80
INPUT1 = """AAAA
BBCD
BBCC
EEEC
"""

# fencing price = 772
# fencing price with discount = 436
INPUT2 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""

# fencing price = 1930
# fencing price with discount = 1206
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

# fencing price with discount = 236
INPUT4 = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
"""

# fencing price with discount = 368
INPUT5 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""


@ddt
class TestIndex10(TestCase):
    @data(
        {'input': INPUT1, 'expected': 140},
        {'input': INPUT2, 'expected': 772},
        {'input': INPUT3, 'expected': 1930},
    )
    @unpack
    def test_get_price_of_fencing(self, input: str, expected: int):
        clusters = set_up(input)
        result = get_price_of_fencing(clusters)
        self.assertEqual(result, expected)

    @data(
        {'input': INPUT1, 'expected': 80},
        {'input': INPUT2, 'expected': 436},
        {'input': INPUT3, 'expected': 1206},
        {'input': INPUT4, 'expected': 236},
        {'input': INPUT5, 'expected': 368},
    )
    @unpack
    def test_get_price_of_fencing_with_discount(self, input: str, expected: int):
        clusters = set_up(input)
        result = get_price_of_fencing_with_discount(clusters)
        self.assertEqual(result, expected)
