import re
from typing import Optional


class LoopException(Exception):
    pass


class Guard:
    def __init__(self, init_x, init_y):
        self.init_x = init_x
        self.init_y = init_y
        # caches for drawings
        self.path_positions = []
        self.path_directions = []
        self.obstacle_placements = []

    def get_distinct_positions_count(self, obstacles: dict[int, list[int]], map_size: tuple[int, int]):
        self.path_positions, self.path_directions = self._do_simulation(obstacles, map_size)
        return len(set(self.path_positions))

    def get_additional_obstacle_positions_which_makes_guard_looping(
        self, obstacles: dict[int, list[int]], map_size: tuple[int, int], draw_on_loop: bool = False,
    ):
        if not self.path_positions:
            self.path_positions, self.path_directions = self._do_simulation(obstacles, map_size)

        obstacle_placements = []
        all_positions_len = len(self.path_positions) - 1
        for idx, (x, y) in enumerate(self.path_positions[1:]):
            print(f'({x}, {y}) [{idx + 1} / {all_positions_len}] ...', end='\r')
            if self._check_loop(obstacles, map_size, x, y, draw_on_loop):
                obstacle_placements.append((x, y))
            print(f'({x}, {y}) [{idx + 1} / {all_positions_len}] - DONE')

        self.obstacle_placements = set(obstacle_placements)
        return len(self.obstacle_placements)

    def _check_loop(
        self, obstacles: dict[int, list[int]], map_size: tuple[int, int], x: int, y: int, draw_on_loop: bool = False,
    ):
        new_obstacles = obstacles.copy()
        new_obstacles[y] = obstacles[y].copy() + [x]
        try:
            self._do_simulation(
                new_obstacles, map_size, detect_loops=True, draw_on_loop=draw_on_loop, special_draw=[(x, y, 'O')],
            )
        except LoopException:
            return True
        return False

    def _do_simulation(
        self,
        obstacles: dict[int, list[int]],
        map_size: tuple[int, int],
        detect_loops=False,
        draw_on_loop=False,
        special_draw=None,
    ):
        x, y = self.init_x, self.init_y
        max_x, max_y = map_size[0] - 1, map_size[1] - 1
        # we start by moving up
        direction = (0, -1)

        path_positions: list[tuple[int, int]] = [(x, y)]
        path_directions: list[tuple[int, int]] = [direction]

        while 0 < x < max_x and 0 < y < max_y:
            x, y, direction = self._simulation_step(x, y, direction, obstacles)
            if detect_loops:
                self._raise_on_loop(
                    x, y, direction, map_size, obstacles, path_positions, path_directions, draw_on_loop, special_draw,
                )
            path_positions.append((x, y))
            path_directions.append(direction)

        return path_positions, path_directions

    def _simulation_step(self, x, y, direction, obstacles):
        new_x, new_y = self._get_new_position(x, y, direction)
        if self._is_colliding(obstacles, new_x, new_y):
            new_direction = self._get_new_direction(direction)
            return x, y, new_direction
        return new_x, new_y, direction

    def _is_colliding(self, obstacles, new_x, new_y):
        return new_x in obstacles.get(new_y, [])

    def _get_new_position(self, x, y, direction):
        return x + direction[0], y + direction[1]

    @staticmethod
    def _get_new_direction(direction: tuple[int, int]):
        """returns the direction rotated 90 degrees clockwise"""
        x, y = direction
        return (-y, x)

    def _raise_on_loop(self, x, y, direction, map_size, obstacles, path_positions, path_directions, draw, special_draw):
        if ((x, y), direction) in zip(path_positions, path_directions):
            if draw:
                MapDrawer.draw_map(path_positions, path_directions, map_size, obstacles, special_draw)
            raise LoopException


class MapParser:
    @staticmethod
    def get_obstacles(data: str):
        return {
            y: [match.start() for match in re.finditer('#', line)]
            for y, line in enumerate(data.split('\n'))
        }

    @staticmethod
    def get_guard(data: str):
        return next(
            (line.index('^'), y)
            for y, line in enumerate(data.split('\n'))
            if '^' in line
        )

    @staticmethod
    def get_map_size(data: str):
        return len(data.split('\n')[0]), len(data.split('\n'))


class MapDrawer:
    @staticmethod
    def draw_map(
        positions: list[tuple[int, int]],
        directions: list[tuple[int, int]],
        map_size: tuple[int, int],
        obstacles: dict[int, list[int]],
        special_items: Optional[list[tuple[int, int, str]]] = None,
    ):
        map = [[' ' for _ in range(map_size[0])] for _ in range(map_size[1])]
        for y, xs in obstacles.items():
            for x in xs:
                map[y][x] = '#'
        for (x, y), direction in zip(positions, directions):
            map[y][x] = (
                ('+' if map[y][x] == '-' else '|')
                if direction in [(0, -1), (0, 1)]
                else ('+' if map[y][x] == '|' else '-')
            )

        map[positions[0][1]][positions[0][0]] = '^'

        if special_items:
            for x, y, symbol in special_items:
                map[y][x] = symbol

        print(64 * '=')
        print('GUARD PATH:')
        print(f'    {"-" * (map_size[1] + 1)}')
        for line_nr, line in enumerate(map):
            print(f'{line_nr:>3} |{"".join(line)}| {line_nr}')
        print(f'    {"-" * (map_size[1] + 1)}')
        print(64 * '=')


def set_up(data: str):
    obstacles = MapParser.get_obstacles(data)
    guard_init_pos = MapParser.get_guard(data)
    map_size = MapParser.get_map_size(data)
    guard = Guard(*guard_init_pos)
    return guard, obstacles, map_size


def get_distinct_guard_positions_count(guard: Guard, obstacles: dict[int, list[int]], map_size: tuple[int, int]):
    return guard.get_distinct_positions_count(obstacles, map_size)


def get_additional_obstacle_positions_which_makes_guard_looping(
    guard: Guard, obstacles: dict[int, list[int]], map_size: tuple[int, int], draw_on_loop: bool = False
):
    return guard.get_additional_obstacle_positions_which_makes_guard_looping(obstacles, map_size, draw_on_loop)


def main(data):
    guard, obstacles, map_size = set_up(data)
    distinct_positions_count = get_distinct_guard_positions_count(guard, obstacles, map_size)
    MapDrawer.draw_map(guard.path_positions, guard.path_directions, map_size, obstacles)
    additional_obstacle_positions_which_makes_guard_looping = (
        get_additional_obstacle_positions_which_makes_guard_looping(guard, obstacles, map_size)
    )
    print(f'Distinct positions count: {distinct_positions_count}')
    print('Additional obstacle positions which makes guard looping: '
          f'{additional_obstacle_positions_which_makes_guard_looping}')


if __name__ == '__main__':
    with open('06_guard_gallivant/input', 'r') as f:
        data = f.read()

    main(data)
