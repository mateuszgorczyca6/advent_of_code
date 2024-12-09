import sys

sys.path.append('.')

from common.grid import Grid, Vector2DPairsValueMapping  # noqa: E402


def set_up(data: str):
    map = Grid(data)
    antennas_pairs_by_value = map.vectors_pairs_by_value
    return map, antennas_pairs_by_value


def get_unique_locations_with_antinode_count(antennas_pairs_by_value: Vector2DPairsValueMapping):
    return len({
        antinode
        for pairs in antennas_pairs_by_value.values()
        for pair in pairs
        for i1, i2 in [(0, 1), (1, 0)]
        if (antinode := pair[i1] * 2 - pair[i2]).is_in_bounds()
    })


def get_unique_locations_with_extended_antinode_count(map: Grid, antennas_pairs_by_value: Vector2DPairsValueMapping):
    return len({
        antinode
        for pairs in antennas_pairs_by_value.values()
        for pair in pairs
        for i1, i2 in [(0, 1), (1, 0)]
        for n in range(1, max(map.width, map.height) - 1)
        if (antinode := pair[i1] * n - pair[i2] * (n-1)).is_in_bounds()
    })


def main(data: str):
    map, antennas_pairs_by_value = set_up(data)
    unique_locations_with_antinode_count = get_unique_locations_with_antinode_count(antennas_pairs_by_value)
    print(f'Unique locations with antinode count: {unique_locations_with_antinode_count}')
    unique_locations_with_extended_antinode_count = get_unique_locations_with_extended_antinode_count(
        map, antennas_pairs_by_value,
    )
    print(f'Unique locations with extended antinode count: {unique_locations_with_extended_antinode_count}')


if __name__ == '__main__':
    with open('08_resonant_collinearity/input', 'r') as f:
        data = f.read()

    main(data)
