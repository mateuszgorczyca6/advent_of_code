from abc import ABCMeta, abstractmethod
from itertools import product


class Letter(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def get_xmassiness(cls, x: int, y: int, data: list[list[str]]) -> int:
        pass

    @classmethod
    def _match_letter(cls, x, y, data, expected):
        return cls._get_letter(x, y, data) == expected

    @staticmethod
    def _get_letter(x, y, data):
        if y < 0 or y >= len(data) or x < 0 or x >= len(data[y]):
            return ''
        return data[y][x]


class XInXMAS(Letter):
    @classmethod
    def get_xmassiness(cls, x: int, y: int, data: list[list[str]]) -> int:
        dirs = product([-1, 0, 1], repeat=2)

        return sum([
            cls._is_mas((dir_x, dir_y), x, y, data)
            for dir_x, dir_y in dirs
        ])

    @classmethod
    def _is_mas(
        cls, dir: tuple[int, int], x: int, y: int, data: list[list[str]],
    ) -> int:
        m_pos = (x+dir[0], y+dir[1])
        a_pos = (x+dir[0]*2, y+dir[1]*2)
        s_pos = (x+dir[0]*3, y+dir[1]*3)
        return all([
            cls._match_letter(*m_pos, data, 'M'),
            cls._match_letter(*a_pos, data, 'A'),
            cls._match_letter(*s_pos, data, 'S'),
        ])


class AINX_MAS(Letter):
    @classmethod
    def get_xmassiness(cls, x: int, y: int, data: list[list[str]]) -> int:
        dirs = product([-1, 1], repeat=2)

        # A can be only once in the middle, but it counts if there are 2 MAS around
        return sum([
            cls._is_mas((dir_x, dir_y), x, y, data)
            for dir_x, dir_y in dirs
        ]) == 2

    @classmethod
    def _is_mas(
        cls, dir: tuple[int, int], x, y, data: list[list[str]],
    ) -> int:
        m_pos = (x+dir[0], y+dir[1])
        s_pos = (x-dir[0], y-dir[1])
        return all([
            cls._match_letter(*m_pos, data, 'M'),
            cls._match_letter(*s_pos, data, 'S'),
        ])


class XMassCounter:
    def __init__(self, data):
        self.array2d_data = [list(y) for y in data.split('\n')]

    def get_xmas_count(self):
        return self._get_common_x_mas_count(XInXMAS, 'X')

    def get_x_mas_count(self):
        return self._get_common_x_mas_count(AINX_MAS, 'A')

    def _get_common_x_mas_count(self, Class: type[Letter], letter: str):
        return sum(
            Class.get_xmassiness(x, y, self.array2d_data)
            for y in range(len(self.array2d_data))
            for x in range(len(self.array2d_data[y]))
            if self.array2d_data[y][x] == letter
        )


if __name__ == '__main__':
    with open('04_ceres_search/input', 'r') as f:
        data = f.read()
    counter = XMassCounter(data)
    print(f'XMAS count: {counter.get_xmas_count()}')
    print(f'X-MAS count: {counter.get_x_mas_count()}')
