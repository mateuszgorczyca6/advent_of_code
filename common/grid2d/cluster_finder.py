from itertools import chain
from typing import TYPE_CHECKING, Callable
import sys

sys.path.append('.')

if TYPE_CHECKING:
    from common.grid2d.grid import Grid
    from common.grid2d.vector import Vector2D


class ClusterFinder:
    def __init__(self, grid: 'Grid'):
        self.grid = grid

    def find_clusters(self, starting_value: str, step_condition: Callable[[str, str], bool]):
        starting_nodes = self.grid.vectors_by_value[starting_value]
        clusters: list['set[Vector2D]'] = []
        for node in starting_nodes:
            if node not in chain.from_iterable(clusters):
                cluster = self._find_cluster(node, step_condition)
                clusters.append(cluster)
        return clusters

    def _find_cluster(
        self,
        node: 'Vector2D',
        step_condition: Callable[[str, str], bool],
        already_checked: set['Vector2D'] = set(),
    ):
        DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        cluster = {node}
        already_checked = {node, *already_checked}
        for direction in DIRECTIONS:
            neighbor = self.grid.position_to_vector.get((node.x + direction[0], node.y + direction[1]))
            if (
                neighbor
                and neighbor.is_in_bounds()
                and neighbor not in already_checked
                and step_condition(node.value, neighbor.value)
            ):
                cluster.update(self._find_cluster(neighbor, step_condition, already_checked))
        return cluster
