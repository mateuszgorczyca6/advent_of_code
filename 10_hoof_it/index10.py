import sys


sys.path.append('.')

from common.grid2d.cluster_finder import ClusterFinder  # noqa: E402
from common.grid2d.grid import Grid  # noqa: E402
from common.grid2d.path_finder import PathFinder  # noqa: E402


def set_up(data: str):
    grid = Grid(data)
    return grid


def get_sum_of_scores(grid: Grid):
    cluster_finder = ClusterFinder(grid)
    clusters = cluster_finder.find_clusters('0', lambda a, b: int(b)-int(a) == 1)
    sum_of_scores = 0
    for cluster in clusters:
        no_of_1 = [1 for vector in cluster if vector.value == '0']
        no_od_9 = [1 for vector in cluster if vector.value == '9']
        sum_of_scores += sum(no_of_1) * sum(no_od_9)
    return sum_of_scores


def get_sum_of_ratings(grid: Grid):
    path_finder = PathFinder(grid)
    paths = path_finder.find_paths_by_value('0', '9', lambda a, b: int(b)-int(a) == 1)
    return len(paths)


def main(data: str):
    grid = set_up(data)
    sum_of_scores = get_sum_of_scores(grid)
    sum_of_ratings = get_sum_of_ratings(grid)
    print(f'Sum of scores: {sum_of_scores}')
    print(f'Sum of ratings: {sum_of_ratings}')


if __name__ == '__main__':
    with open('10_hoof_it/input', 'r') as f:
        data = f.read()

    main(data)
