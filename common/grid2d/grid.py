from collections import defaultdict
from itertools import combinations
from typing import TYPE_CHECKING, Optional
import sys

sys.path.append('.')

from common.grid2d.vector import Vector2D  # noqa: E402

if TYPE_CHECKING:
    from common.grid2d.types import (
        PositionToVector2DMapping,
        Vector2DList,
        Vector2DValueMapping,
        Vector2DPairsValueMapping,
    )


class Grid:
    def __init__(self, data: str):
        self.data = data
        lines = [line for line in data.split('\n') if line != '']
        self.width = len(lines[0])
        self.height = len(lines)

        self._vectors: Optional['Vector2DList'] = None
        self._position_to_vector: Optional['PositionToVector2DMapping'] = None
        self._vectors_by_value: Optional['Vector2DValueMapping'] = None
        self._vectors_pairs_by_value: Optional['Vector2DPairsValueMapping'] = None

    def clear_cache(self):
        self._vectors = None
        self._position_to_vector = None
        self._vectors_by_value = None
        self._vectors_pairs_by_value = None

    @property
    def vectors(self) -> 'Vector2DList':
        if self._vectors is None:
            self._vectors = self.get_vectors(self.data)
        return self._vectors

    @property
    def position_to_vector(self) -> 'PositionToVector2DMapping':
        if self._position_to_vector is None:
            self._position_to_vector = self.get_position_to_vector()
        return self._position_to_vector

    @property
    def vectors_by_value(self) -> 'Vector2DValueMapping':
        if self._vectors_by_value is None:
            self._vectors_by_value = self.get_vectors_by_value(self.data)
        return self._vectors_by_value

    @property
    def vectors_pairs_by_value(self) -> 'Vector2DPairsValueMapping':
        if self._vectors_pairs_by_value is None:
            self._vectors_pairs_by_value = self.get_vectors_pairs_by_value(self.data)
        return self._vectors_pairs_by_value

    def add_vector(self, vector: Vector2D):
        old_vector = self.position_to_vector.get((vector.x, vector.y))
        if old_vector is not None:
            old_vector.value = vector.value
        else:
            self.vectors.append(vector)

    def get_vectors(self, data: str) -> 'Vector2DList':
        vectors = [
            Vector2D(x, y, value, self)
            for y, line in enumerate(data.split('\n'))
            for x, value in enumerate(line)
            if value != '.'
        ]
        return vectors

    def get_position_to_vector(self) -> 'PositionToVector2DMapping':
        return {
            (vector.x, vector.y): vector
            for vector in self.vectors
        }

    def get_vectors_by_value(self, data: str) -> 'Vector2DValueMapping':
        mapping = defaultdict(set)
        vectors = self.get_vectors(data)

        for vector in vectors:
            mapping[vector.value].add(vector)
        return mapping

    def get_vectors_pairs_by_value(self, data: str) -> 'Vector2DPairsValueMapping':
        mapping = defaultdict(set)
        vectors_by_value = self.get_vectors_by_value(data)
        for value, vectors in vectors_by_value.items():
            pairs = combinations(vectors, 2)
            mapping[value] = set(pairs)
        return mapping

    def __str__(self):
        array2d_data = [
            ['.'] * self.width
            for _ in range(self.height)
        ]
        for vector in self.vectors:
            array2d_data[vector.y][vector.x] = vector.value
        return '\n'.join([''.join(line) for line in array2d_data])
