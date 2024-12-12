from collections import defaultdict
from typing import TYPE_CHECKING, Literal
import sys

sys.path.append('.')

if TYPE_CHECKING:
    from common.grid2d.clusters import Cluster
    from common.grid2d.vector import Vector2D


GroupedBorders = dict[Literal['v', 'h'], dict[int, dict[bool, list['ClusterBorder']]]]


class ClusterBorder:
    def __init__(self, orientation: Literal['v', 'h'], index: int, is_index_inside: bool, range: tuple[int, int]):
        """Border exists right before the index."""
        self.orientation: Literal['v', 'h'] = orientation
        self.is_index_inside = is_index_inside
        self.index = index
        self.range = range

    def __repr__(self):
        return f'Border({self.orientation}, {self.index}, {self.range})'


class ClusterBorderFinder:
    @classmethod
    def get_borders(cls, cluster: 'Cluster'):
        """Borders around the cluster. Note that if there is a situation as follow:

        ```
        AAAA
        ABAA
        AABA
        AAAA
        ```

        There cluster with `A` have 8 borders which goes around `B` clusters (and 4 around itself).
        The middle one is counted as 2.
        """
        singular_borders = cls._get_singular_borders(cluster)
        grouped_borders = cls._get_grouped_borders(singular_borders)
        return cls._get_full_borders(grouped_borders)

    @classmethod
    def _get_singular_borders(cls, cluster: 'Cluster'):
        return [
            cls._get_singular_border(vector, neighbor, idx)
            for vector in cluster
            for idx, neighbor in enumerate(vector.neighbors)
            if neighbor not in cluster
        ]

    @staticmethod
    def _get_singular_border(vector: 'Vector2D', neighbor: 'Vector2D', idx: int):
        orientation = 'v' if idx <= 1 else 'h'
        idx_source = vector if idx in {0, 2} else neighbor
        idx = idx_source.x if orientation == 'h' else idx_source.y
        is_index_inside = idx_source is vector
        range_position = idx_source.x if orientation == 'v' else idx_source.y
        return ClusterBorder(orientation, idx, is_index_inside, (range_position, range_position))

    @staticmethod
    def _get_grouped_borders(singular_borders: list[ClusterBorder]):
        grouped_borders: GroupedBorders = (defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
        for border in singular_borders:
            grouped_borders[border.orientation][border.index][border.is_index_inside].append(border)
        return grouped_borders

    @classmethod
    def _get_full_borders(cls, grouped_borders: GroupedBorders):
        full_borders: list[ClusterBorder] = []
        for orientation, index_to_is_index_inside in grouped_borders.items():
            for index, is_index_inside_to_borders in index_to_is_index_inside.items():
                for is_index_inside, borders in is_index_inside_to_borders.items():
                    new_borders = cls._get_full_borders_from_single_group(borders, orientation, index, is_index_inside)
                    full_borders.extend(new_borders)
        return full_borders

    @staticmethod
    def _get_full_borders_from_single_group(
        borders: list[ClusterBorder], orientation: Literal['v', 'h'], index: int, is_index_inside: bool,
    ):
        new_borders = []
        sorted_borders = sorted(borders, key=lambda border: border.range[0])
        new_border = None
        for border in sorted_borders:
            if (new_border is not None) and (new_border.range[1] + 1 == border.range[0]):
                new_border.range = (border.range[0], border.range[1])
            else:
                if new_border is not None:
                    new_borders.append(new_border)
                new_border = ClusterBorder(orientation, index, is_index_inside, border.range)
        if new_border is not None:
            new_borders.append(new_border)
        return new_borders
