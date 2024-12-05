from unittest import TestCase

from index05 import get_average_middle_page_number, get_average_middle_page_number_for_fixed_wrong_updates, set_up

AGGREGATOR_INPUT = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


class TestGetAverageMiddlePageNumber(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page_number_set, cls.update_set = set_up(AGGREGATOR_INPUT)
        super().setUpClass()

    def test_get_average_middle_page_number(self):
        result = get_average_middle_page_number(self.page_number_set, self.update_set)
        self.assertEqual(result, 143)

    def test_get_average_middle_page_number_for_fixed_wrong_updates(self):
        result = get_average_middle_page_number_for_fixed_wrong_updates(self.page_number_set, self.update_set)
        self.assertEqual(result, 123)
