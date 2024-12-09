from collections import defaultdict
from itertools import combinations
from typing import Optional


class Vector2D:
    """Note that vectors are equal when have the same x and y coordinates. Name and grid do not matter."""
    def __init__(self, x: int, y: int, value: str, grid: 'Grid'):
        self.x = x
        self.y = y
        self.value = value
        self.grid = grid

    def is_in_bounds(self):
        return 0 <= self.x < self.grid.width and 0 <= self.y < self.grid.height

    def copy(self):
        return Vector2D(self.x, self.y, self.value, self.grid)

    def __sub__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y, self.value, self.grid)
        return self.copy()

    def __add__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y, self.value, self.grid)
        return self.copy()

    def __mul__(self, other):
        if isinstance(other, int):
            return Vector2D(self.x * other, self.y * other, self.value, self.grid)
        return self.copy()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f'({self.x}, {self.y})'


class Grid:
    def __init__(self, data: str):
        self.data = data
        lines = [line for line in data.split('\n') if line != '']
        self.width = len(lines[0])
        self.height = len(lines)

        self._vectors: Optional[list[Vector2D]] = None
        self._vectors_by_value: Optional[dict[str, set[Vector2D]]] = None
        self._vectors_pairs_by_value: Optional[dict[str, set[tuple[Vector2D, Vector2D]]]] = None

    @property
    def vectors(self) -> list[Vector2D]:
        if self._vectors is None:
            self._vectors = self.get_vectors(self.data)
        return self._vectors

    @property
    def vectors_by_value(self) -> dict[str, set[Vector2D]]:
        if self._vectors_by_value is None:
            self._vectors_by_value = self.get_vectors_by_value(self.data)
        return self._vectors_by_value

    @property
    def vectors_pairs_by_value(self) -> dict[str, set[tuple[Vector2D, Vector2D]]]:
        if self._vectors_pairs_by_value is None:
            self._vectors_pairs_by_value = self.get_same_value_vectors_pairs(self.data)
        return self._vectors_pairs_by_value

    def get_vectors(self, data: str) -> list[Vector2D]:
        vectors = [
            Vector2D(x, y, value, self)
            for y, line in enumerate(data.split('\n'))
            for x, value in enumerate(line)
            if value != '.'
        ]
        return vectors

    def get_vectors_by_value(self, data: str) -> dict[str, set[Vector2D]]:
        mapping = defaultdict(set)
        vectors = self.get_vectors(data)

        for vector in vectors:
            mapping[vector.value].add(vector)
        return mapping

    def get_same_value_vectors_pairs(self, data: str) -> dict[str, set[tuple[Vector2D, Vector2D]]]:
        mapping = defaultdict(set)
        vectors_by_value = self.get_vectors_by_value(data)
        for value, vectors in vectors_by_value.items():
            pairs = combinations(vectors, 2)
            mapping[value] = set(pairs)
        return mapping
