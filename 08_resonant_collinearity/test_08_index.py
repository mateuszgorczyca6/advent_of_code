from unittest import TestCase
from ddt import ddt, data, unpack

from index08 import get_unique_locations_with_antinode_count


# has 2 antinodes
INPUT1 = """..........
..........
..........
....a.....
..........
.....a....
..........
..........
..........
.........."""


# has 4 antinodes
INPUT2 = """..........
..........
..........
....a.....
........a.
.....a....
..........
..........
..........
.........."""


# has 4 antinodes
INPUT3 = """..........
..........
..........
....a.....
........a.
.....a....
..........
......A...
..........
.........."""


# has 14 antinodes
INPUT4 = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""


# has 1 antinodes
INPUT5 = """......
...b.b
......
.a....
......
.a...."""


@ddt
class TestBridgeRepair(TestCase):
    @data(
        {'input': INPUT1, 'expected': 2},
        {'input': INPUT2, 'expected': 4},
        {'input': INPUT3, 'expected': 4},
        {'input': INPUT4, 'expected': 14},
        {'input': INPUT5, 'expected': 1},
    )
    @unpack
    def test_get_unique_locations_with_antinode_count(self, input: str, expected: int):
        result = get_unique_locations_with_antinode_count(input)
        self.assertEqual(result, expected)
