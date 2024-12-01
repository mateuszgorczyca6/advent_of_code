from ddt import ddt, data, unpack
from unittest import TestCase

from index import get_lists_distance, get_lists_similarity_score


@ddt
class TestGetListsDistance(TestCase):
    @data(
        # 1 - distance is 0 when lists are equal
        {'input': ([1, 2, 3], [1, 2, 3]), 'expected': 0},
        # 2 - distance is 0 when lists are empty
        {'input': ([], []), 'expected': 0},
        # 3 - distance is correct when lists are ordered
        {'input': ([1, 2, 3], [3, 10, 20]), 'expected': 2 + 8 + 17},
        # 4 - distance is correct when lists are not ordered
        {'input': ([2, 1, 3], [10, 20, 3]), 'expected': 2 + 8 + 17},
    )
    @unpack
    def test_get_lists_distance(self, input: tuple[list[int], list[int]], expected: int):
        result = get_lists_distance(*input)
        self.assertEqual(result, expected)


@ddt
class TestGetListsSimilarityScore(TestCase):
    @data(
        # 1 - distance is 0 when lists are empty
        {'input': ([], []), 'expected': 0},
        # 2 - distance is correct
        {'input': ([1, 2, 3, 4], [1, 1, 2, 3, 3, 3]), 'expected': 1*2+2*1+3*3+4*0},
    )
    @unpack
    def test_get_lists_similarity_score(self, input: tuple[list[int], list[int]], expected: int):
        result = get_lists_similarity_score(*input)
        self.assertEqual(result, expected)
