from typing import TYPE_CHECKING
import sys

sys.path.append('.')


if TYPE_CHECKING:
    from common.grid2d.vector import Vector2D  # noqa: F401


Vector2DList = list['Vector2D']
PositionToVector2DMapping = dict[tuple[int, int], 'Vector2D']
Vector2DValueMapping = dict[str, set['Vector2D']]
Vector2DPairsValueMapping = dict[str, set[tuple['Vector2D', 'Vector2D']]]
