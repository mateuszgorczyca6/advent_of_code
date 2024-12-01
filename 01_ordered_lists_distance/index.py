from collections import Counter
import re


def get_lists_distance(list1: list, list2: list) -> int:
    list1_sorted = sorted(list1)
    list2_sorted = sorted(list2)
    return sum(abs(x - y) for x, y in zip(list1_sorted, list2_sorted))


def get_lists_similarity_score(list1: list, list2: list) -> int:
    list2_counts = Counter(list2)
    return sum(map(lambda x: x * list2_counts[x], list1))


if __name__ == '__main__':
    list1 = []
    list2 = []
    with open('01_1_ordered_lists_distance/input', 'r') as f:
        for line in f.readlines():
            match = re.match(r'(\d+)\s+(\d+)', line)
            if match:
                val1, val2 = match.groups()
                list1.append(int(val1))
                list2.append(int(val2))
    print(f'distance: {get_lists_distance(list1, list2)}')
    print(f'similarity: {get_lists_similarity_score(list1, list2)}')
