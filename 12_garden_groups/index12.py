import sys

sys.path.append('.')

from common.grid2d.clusters import Cluster, SeparatedClusterFinder  # noqa: E402
from common.grid2d.grid import Grid  # noqa: E402


def set_up(raw_data: str):
    grid = Grid(raw_data)
    cluster_finder = SeparatedClusterFinder(grid)
    clusters = cluster_finder.find_clusters(lambda a, b: a == b)
    return clusters


def get_price_of_fencing(clusters: list[Cluster]):
    return sum(
        cluster.area * cluster.perimeter
        for cluster in clusters
    )


def get_price_of_fencing_with_discount(clusters: list[Cluster]):
    return sum(
        cluster.area * len(cluster.borders)
        for cluster in clusters
    )


def main(data: str):
    clusters = set_up(data.strip())
    price_of_fencing = get_price_of_fencing(clusters)
    print(f'Price of fencing: {price_of_fencing}')
    price_of_fencing_with_discount = get_price_of_fencing_with_discount(clusters)
    print(f'Price of fencing with discount: {price_of_fencing_with_discount}')


if __name__ == '__main__':
    with open('12_garden_groups/input', 'r') as f:
        data = f.read()

    main(data)
