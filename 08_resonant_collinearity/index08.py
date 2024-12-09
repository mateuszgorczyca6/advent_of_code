import sys

sys.path.append('.')

from common.grid import Grid  # noqa: E402


def get_unique_locations_with_antinode_count(data: str):
    map = Grid(data)
    antennas_pairs_by_value = map.get_same_value_vectors_pairs(data)
    antinodes = set()

    antinodes = {
        antinode
        for pairs in antennas_pairs_by_value.values()
        for pair in pairs
        for i1, i2 in [(0, 1), (1, 0)]
        if (antinode := pair[i1] * 2 - pair[i2]).is_in_bounds()
    }
    return len(antinodes)


def main(data: str):
    unique_locations_with_antinode_count = get_unique_locations_with_antinode_count(data)
    print(f'Unique locations with antinode count: {unique_locations_with_antinode_count}')


if __name__ == '__main__':
    with open('08_resonant_collinearity/input', 'r') as f:
        data = f.read()

    main(data)
