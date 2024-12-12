from functools import cache
import math


class StonesCounter:
    def __init__(self, data: list[int]) -> None:
        self.data = data

    def get_stones_count(self, blinks: int):
        return sum([
            self._get_stone_count(stone, blinks, 0)
            for stone in self.data
        ])

    @cache
    def _get_stone_count(self, stone: int, blinks: int, age: int = 0):
        if age == blinks:
            return 1

        age += 1

        if stone == 0:
            return self._get_stone_count(1, blinks, age)

        if (num_of_digits := int(math.log10(stone)) + 1) % 2 == 0:
            stone1, stone2 = divmod(stone, pow(10, num_of_digits // 2))
            return sum([
                self._get_stone_count(stone1, blinks, age),
                self._get_stone_count(stone2, blinks, age),
            ])

        return self._get_stone_count(stone * 2024, blinks, age)


def get_num_of_stones(raw_data: str, blinks: int):
    data = list(map(int, raw_data.strip().split(' ')))
    stones_counter = StonesCounter(data)
    return stones_counter.get_stones_count(blinks)


def main(data: str):
    num_of_stones_25 = get_num_of_stones(data, 25)
    print(f'Num of stones after 25 blinks: {num_of_stones_25}')
    num_of_stones_75 = get_num_of_stones(data, 75)
    print(f'Num of stones after 75 blinks: {num_of_stones_75}')


if __name__ == '__main__':
    with open('11_plutonian_pebbles/input', 'r') as f:
        data = f.read()

    main(data)
