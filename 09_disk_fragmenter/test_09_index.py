from unittest import TestCase

from index09 import get_filesystem_checksum

# has 2 antinodes
INPUT = """2333133121414131402
"""


class TestBridgeRepair(TestCase):
    def test_get_unique_locations_with_antinode_count(self):
        result = get_filesystem_checksum(INPUT)
        self.assertEqual(result, 1928)
