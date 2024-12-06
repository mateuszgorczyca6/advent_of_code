from unittest import TestCase

from index06 import (
    get_additional_obstacle_positions_which_makes_guard_looping,
    get_distinct_guard_positions_count,
    set_up,
)


INPUT_DATA = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


class TestGetAverageMiddlePageNumber(TestCase):
    def test_get_average_middle_page_number(self):
        guard, obstacles, map_size = set_up(INPUT_DATA)
        result = get_distinct_guard_positions_count(guard, obstacles, map_size)
        self.assertEqual(result, 41)

    def test_get_additional_obstacle_positions_which_makes_guard_looping(self):
        guard, obstacles, map_size = set_up(INPUT_DATA)
        result = get_additional_obstacle_positions_which_makes_guard_looping(guard, obstacles, map_size, True)
        self.assertEqual(result, 6)
