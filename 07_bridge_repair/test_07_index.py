from unittest import TestCase
from index07 import get_total_calibration_result


INPUT = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""


class TestBridgeRepair(TestCase):
    def test_get_total_calibration_result(self):
        self.assertEqual(get_total_calibration_result(INPUT), 3749)
