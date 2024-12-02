from ddt import ddt, data, unpack
from unittest import TestCase

from index02 import get_safe_reports_count, get_weak_safe_reports_count


@ddt
class TestGetListsDistance(TestCase):
    @data(
        # 1 - 0 when there are no reports
        {'input': [], 'expected': 0},
        # 2 - safe report when all conditions are met (ascending)
        {'input': ['1 2 3'], 'expected': 1},
        # 3 - safe report when all conditions are met (descending)
        {'input': ['8 5 2'], 'expected': 1},
        # 4 - dangerous report when not ascending nor descending
        {'input': ['1 3 2'], 'expected': 0},
        # 4 - dangerous report when not spacing too small
        {'input': ['1 1 2'], 'expected': 0},
        # 4 - dangerous report when not spacing too big
        {'input': ['1 5 6'], 'expected': 0},
    )
    @unpack
    def test_get_safe_reports_count(self, input: list[str], expected: int):
        result = get_safe_reports_count(input)
        self.assertEqual(result, expected)

    @data(
        # 1 - safe report when is strongly safe
        {'input': ['1 2 3 4'], 'expected': 1},
        # 2 - safe report when removing one number will fix it
        {'input': ['1 4 3 4'], 'expected': 1},
        # 3 - dangerous report when removing two number will fix it
        {'input': ['1 4 3 10'], 'expected': 0},
    )
    @unpack
    def test_get_weak_safe_reports_count(self, input: list[str], expected: int):
        result = get_weak_safe_reports_count(input)
        self.assertEqual(result, expected)
