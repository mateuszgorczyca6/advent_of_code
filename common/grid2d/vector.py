from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from common.grid2d.grid import Grid


class Vector2D:
    """Note that vectors are equal when have the same x and y coordinates. Name and grid do not matter."""
    def __init__(self, x: int, y: int, value: str, grid: 'Grid'):
        self.x = x
        self.y = y
        self.value = value
        self.grid = grid

    @property
    def neighbors(self):
        DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        return [
            Vector2D(self.x + dx, self.y + dy, self.value, self.grid)
            for dx, dy in DIRECTIONS
        ]

    def is_in_bounds(self):
        return 0 <= self.x < self.grid.width and 0 <= self.y < self.grid.height

    def copy(self):
        return Vector2D(self.x, self.y, self.value, self.grid)

    def __sub__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y, self.value, self.grid)
        if isinstance(other, tuple) and len(other) == 2:
            return Vector2D(self.x - other[0], self.y - other[1], self.value, self.grid)
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
