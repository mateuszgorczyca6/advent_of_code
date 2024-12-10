from collections import deque
import sys

sys.path.append('.')


def get_filesystem_checksum(data: str):
    data = data.strip()

    filesystem = deque()
    dots_idxs = deque()
    for idx, value in enumerate(data):
        value = int(value)
        for _ in range(value):
            if idx % 2 == 0:
                filesystem.append(idx // 2)
            else:
                filesystem.append('.')
                dots_idxs.append(len(filesystem) - 1)

    right_idx = len(filesystem) - 1
    for left_idx in dots_idxs:
        right_value = '.'
        while right_value == '.':
            right_value = filesystem[right_idx]
            right_idx -= 1

        filesystem[left_idx] = right_value

        if left_idx >= right_idx:
            break

    for idx in range(right_idx + 2, len(filesystem)):
        filesystem[idx] = '.'

    return sum(idx * value for idx, value in enumerate(filesystem) if value != '.')


def main(data: str):
    filesystem_checksum = get_filesystem_checksum(data)
    print(f'Filesystem checksum: {filesystem_checksum}')


if __name__ == '__main__':
    with open('09_disk_fragmenter/input', 'r') as f:
        data = f.read()

    main(data)
