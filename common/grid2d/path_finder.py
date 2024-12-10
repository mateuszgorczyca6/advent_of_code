from typing import TYPE_CHECKING, Callable
import sys

sys.path.append('.')

from common.grid2d.abstract_finder import AbstractFinder  # noqa: E402

if TYPE_CHECKING:
    from common.grid2d.vector import Vector2D


class PathFinder(AbstractFinder):
    def find_paths_by_value(self, starting_value: str, final_value: str, step_condition: Callable[[str, str], bool]):
        starting_nodes = self.grid.vectors_by_value[starting_value]
        paths: list[list['Vector2D']] = []
        for node in starting_nodes:
            path = self._find_paths_by_value(node, final_value, step_condition)
            paths.extend(path)
        return paths

    def _find_paths_by_value(
        self,
        node: 'Vector2D',
        final_value: str,
        step_condition: Callable[[str, str], bool],
        visited_nodes: set['Vector2D'] = set(),
    ):
        paths: list[list['Vector2D']] = []
        self._spread_walking(node, step_condition, paths, visited_nodes, final_value)
        return paths

    def _action_on_neighbor_node(
        self,
        neighbor: 'Vector2D',
        paths: list[list['Vector2D']],
        step_condition: Callable[[str, str], bool],
        visited_nodes: set['Vector2D'],
        final_value: str
    ):
        if neighbor.value == final_value:
            paths.append([*visited_nodes, neighbor])
        paths.extend(self._find_paths_by_value(neighbor, final_value, step_condition, visited_nodes))
