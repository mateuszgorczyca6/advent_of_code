import re


class Guard:
    def __init__(self, init_x, init_y):
        self.init_x = init_x
        self.init_y = init_y
        # caches for drawings
        self.path_positions = []
        self.path_directions = []

    def get_distinct_positions_count(self, obstacles: dict[int, list[int]], map_size: tuple[int, int]):
        self.path_positions, self.path_directions = self._do_simulation(obstacles, map_size)
        return len(set(self.path_positions))

    def _do_simulation(self, obstacles: dict[int, list[int]], map_size: tuple[int, int]):
        x, y = self.init_x, self.init_y
        max_x, max_y = map_size[0] - 1, map_size[1] - 1
        # we start by moving up
        direction = (0, -1)

        path_positions: list[tuple[int, int]] = [(x, y)]
        path_directions: list[tuple[int, int]] = [direction]

        while 0 < x < max_x and 0 < y < max_y:
            x, y, direction = self._simulation_step(x, y, direction, obstacles)
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
    def draw_map(guard: Guard, map_size: tuple[int, int], obstacles: dict[int, list[int]]):
        positions = guard.path_positions
        directions = guard.path_directions
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

        map[guard.init_y][guard.init_x] = '^'

        print(64 * '=')
        print('GUARD PATH:')
        print(f'    {'-' * (map_size[1] + 1)}')
        for line_nr, line in enumerate(map):
            print(f'{line_nr:>3} |{"".join(line)}| {line_nr}')
        print(f'    {'-' * (map_size[1] + 1)}')
        print(64 * '=')


def set_up(data: str):
    obstacles = MapParser.get_obstacles(data)
    guard_init_pos = MapParser.get_guard(data)
    map_size = MapParser.get_map_size(data)
    guard = Guard(*guard_init_pos)
    return guard, obstacles, map_size


def get_distinct_guard_positions_count(guard: Guard, obstacles: dict[int, list[int]], map_size: tuple[int, int]):
    return guard.get_distinct_positions_count(obstacles, map_size)


def main(data):
    guard, obstacles, map_size = set_up(data)
    distinct_positions_count = get_distinct_guard_positions_count(guard, obstacles, map_size)
    print(f'Distinct positions count: {distinct_positions_count}')
    # MapDrawer.draw_map(guard, map_size, obstacles)


if __name__ == '__main__':
    with open('06_guard_gallivant/input', 'r') as f:
        data = f.read()

    main(data)
