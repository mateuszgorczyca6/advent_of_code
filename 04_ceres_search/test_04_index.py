from unittest import TestCase
from ddt import ddt, data, unpack

from index04 import XMassCounter


HORIZONTAL_XMAS = """
XMAS..
XMAS..
XMAS..
"""

HORIZONTAL_XMAS_REVERSED = """
.SAMX.
.SAMX.
.SAMX.
"""

VERTICAL_XMAS = """
X.X
M.M
AXA
SMS
.A.
.S.
...
"""

VERTICAL_XMAS_REVERSED = """
...
S.S
A.A
MSM
XAX
.M.
.X.
"""

DIAGONAL_XMAS = """
X.....
.MX...
..AM..
...SA.
.....S
"""

DIAGONAL_XMAS_REVERSED = """
S.....
.AS...
..MA..
...XM.
.....X
"""

X_MAS = """
M.M.M.S.M
.A.A...A.
S.S.S.S.M
.A.A...A.
M.M.M.S.M
"""


@ddt
class TestXMassCounter(TestCase):
    @data(
        # 1 - test for horizontal data
        {'input': HORIZONTAL_XMAS, 'expected': 3},
        # 2 - test for reversed horizontal data
        {'input': HORIZONTAL_XMAS_REVERSED, 'expected': 3},
        # 3 - test for vertical data
        {'input': VERTICAL_XMAS, 'expected': 3},
        # 4 - test for vertical reversed data
        {'input': VERTICAL_XMAS_REVERSED, 'expected': 3},
        # 5 - test for diagonal data
        {'input': DIAGONAL_XMAS, 'expected': 2},
        # 6 - test for diagonal reversed data
        {'input': DIAGONAL_XMAS, 'expected': 2},
    )
    @unpack
    def test_xmass_counter(self, input: str, expected: int):
        result = XMassCounter(input).get_xmas_count()
        self.assertEqual(result, expected)

    def test_x_mass_counter(self):
        result = XMassCounter(X_MAS).get_x_mas_count()
        self.assertEqual(result, 6)
