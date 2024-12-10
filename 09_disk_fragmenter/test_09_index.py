from unittest import TestCase

from index09 import get_filesystem_checksum

# has 2 antinodes
INPUT = """2333133121414131402
"""


class TestBridgeRepair(TestCase):
    def test_get_unique_locations_with_antinode_count(self):
        result1 = get_filesystem_checksum(INPUT, True)
        result2 = get_filesystem_checksum(INPUT, False)
        self.assertEqual(result1, 1928)
        self.assertEqual(result2, 2858)
