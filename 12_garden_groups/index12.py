import sys

sys.path.append('.')

from common.grid2d.cluster_finder import SeparatedClusterFinder  # noqa: E402
from common.grid2d.grid import Grid  # noqa: E402


def get_price_of_fencing(raw_data: str):
    grid = Grid(raw_data)
    cluster_finder = SeparatedClusterFinder(grid)
    clusters = cluster_finder.find_clusters(lambda a, b: a == b)
    return sum(
        cluster.area * cluster.perimeter
        for cluster in clusters
    )


def main(data: str):
    price_of_fencing = get_price_of_fencing(data.strip())
    print(f'Price of fencing: {price_of_fencing}')


if __name__ == '__main__':
    with open('12_garden_groups/input', 'r') as f:
        data = f.read()

    main(data)
