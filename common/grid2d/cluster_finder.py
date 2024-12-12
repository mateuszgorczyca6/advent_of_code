from itertools import chain
from typing import TYPE_CHECKING, Callable, Optional
import sys

sys.path.append('.')

from common.grid2d.abstract_finder import AbstractFinder  # noqa: E402

if TYPE_CHECKING:
    from common.grid2d.vector import Vector2D


class Cluster(set['Vector2D']):
    @property
    def area(self):
        return len(self)

    @property
    def perimeter(self):
        return sum(
            1
            for vector in self
            for neighbor in vector.neighbors
            if neighbor not in self
        )


class ClusterFinder(AbstractFinder):
    def find_clusters(self, step_condition: Callable[[str, str], bool], starting_value: Optional[str] = None):
        """@param starting_value: Only nodes with this value will be used to start the search."""
        self.visited_nodes = set()
        starting_nodes = self.grid.vectors_by_value[starting_value] if starting_value else self.grid.vectors
        clusters: list[Cluster] = []
        for node in starting_nodes:
            if node not in chain.from_iterable(clusters):
                cluster = Cluster(self._find_cluster(node, step_condition))
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


class SeparatedClusterFinder(ClusterFinder):
    def find_clusters(self, step_condition: Callable[[str, str], bool], starting_value: Optional[str] = None):
        self.visited_nodes = set()
        return super().find_clusters(step_condition, starting_value)

    def _spread_walking(
        self,
        node: 'Vector2D',
        step_condition: Callable[[str, str], bool],
        clusters: set['Vector2D'],
        visited_nodes: set['Vector2D'] = set(),
        *args,
        **kwargs,
    ):
        self.visited_nodes.add(node)
        super()._spread_walking(node, step_condition, clusters, visited_nodes, *args, **kwargs)

    def _should_check(
        self,
        node: 'Vector2D',
        neighbor: Optional['Vector2D'],
        visited_nodes: set['Vector2D'],
        step_condition: Callable[[str, str], bool],
    ):
        return (
            super()._should_check(node, neighbor, visited_nodes, step_condition)
            and neighbor not in self.visited_nodes
        )
