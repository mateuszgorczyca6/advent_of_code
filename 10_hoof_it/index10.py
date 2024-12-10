import sys

sys.path.append('.')

from common.grid2d.cluster_finder import ClusterFinder  # noqa: E402
from common.grid2d.grid import Grid  # noqa: E402


def get_sum_of_scores(data: str):
    grid = Grid(data)
    cluster_finder = ClusterFinder(grid)
    clusters = cluster_finder.find_clusters('0', lambda a, b: int(b)-int(a) == 1)
    sum_of_scores = 0
    for cluster in clusters:
        no_of_1 = [1 for vector in cluster if vector.value == '0']
        no_od_9 = [1 for vector in cluster if vector.value == '9']
        sum_of_scores += sum(no_of_1) * sum(no_od_9)
    return sum_of_scores


def main(data: str):
    sum_of_scores = get_sum_of_scores(data)
    print(f'Sum of scores: {sum_of_scores}')


if __name__ == '__main__':
    with open('10_hoof_it/input', 'r') as f:
        data = f.read()

    main(data)
