from unittest import TestCase
from ddt import ddt, data, unpack

from index10 import get_sum_of_scores


# score = 1
INPUT_1 = """0123
1234
8765
9876
"""

# score = 2
INPUT_2 = """...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9
"""

# score = 4
INPUT_3 = """..90..9
...1.98
...2..7
6543456
765.987
876....
987....
"""

# score = 3
INPUT_4 = """10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01
"""

# score = 36
INPUT_5 = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


@ddt
class TestIndex10(TestCase):
    @data(
        {'input': INPUT_1, 'expected': 1},
        {'input': INPUT_2, 'expected': 2},
        {'input': INPUT_3, 'expected': 4},
        {'input': INPUT_4, 'expected': 3},
        {'input': INPUT_5, 'expected': 36},
    )
    @unpack
    def test_get_sum_of_scores(self, input: str, expected: int):
        self.assertEqual(get_sum_of_scores(input), expected)
