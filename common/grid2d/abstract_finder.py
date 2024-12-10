import abc
import sys
from typing import TYPE_CHECKING, Callable, Iterable

sys.path.append('.')

if TYPE_CHECKING:
    from common.grid2d.grid import Grid
    from common.grid2d.vector import Vector2D


class AbstractFinder(metaclass=abc.ABCMeta):
    def __init__(self, grid: 'Grid'):
        self.grid = grid

    def _spread_walking(
        self,
        node: 'Vector2D',
        step_condition: Callable[[str, str], bool],
        aggregator: Iterable,
        visited_nodes: set['Vector2D'] = set(),
        *args,
        **kwargs,
    ):
        DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        visited_nodes = {node, *visited_nodes}
        for direction in DIRECTIONS:
            neighbor = self.grid.position_to_vector.get((node.x + direction[0], node.y + direction[1]))
            if (
                neighbor
                and neighbor.is_in_bounds()
                and neighbor not in visited_nodes
                and step_condition(node.value, neighbor.value)
            ):
                self._action_on_neighbor_node(neighbor, aggregator, step_condition, visited_nodes, *args, **kwargs)

    @abc.abstractmethod
    def _action_on_neighbor_node(
        self,
        neighbor: 'Vector2D',
        aggregator: Iterable,
        step_condition: Callable[[str, str], bool],
        visited_nodes: set['Vector2D'] = set(),
        *args,
        **kwargs,
    ):
        raise NotImplementedError
