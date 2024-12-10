from itertools import chain
from typing import TYPE_CHECKING, Callable
import sys

sys.path.append('.')

from common.grid2d.abstract_finder import AbstractFinder  # noqa: E402

if TYPE_CHECKING:
    from common.grid2d.vector import Vector2D


class ClusterFinder(AbstractFinder):
    def find_clusters(self, starting_value: str, step_condition: Callable[[str, str], bool]):
        starting_nodes = self.grid.vectors_by_value[starting_value]
        clusters: list[set['Vector2D']] = []
        for node in starting_nodes:
            if node not in chain.from_iterable(clusters):
                cluster = self._find_cluster(node, step_condition)
                clusters.append(cluster)
        return clusters

    def _find_cluster(
        self,
        node: 'Vector2D',
        step_condition: Callable[[str, str], bool],
        visited_nodes: set['Vector2D'] = set(),
    ):
        cluster = {node}
        self._spread_walking(node, step_condition, cluster, visited_nodes)
        return cluster

    def _action_on_neighbor_node(
        self,
        neighbor: 'Vector2D',
        clusters: set['Vector2D'],
        step_condition: Callable[[str, str], bool],
        visited_nodes: set['Vector2D'] = set(),
        *args,
        **kwargs,
    ):
        clusters.update(self._find_cluster(neighbor, step_condition, visited_nodes))
