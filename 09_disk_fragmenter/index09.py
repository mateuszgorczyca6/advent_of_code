from collections import deque
import sys

sys.path.append('.')


class DataBlock:
    def __init__(self, value: int, idx: int, size: int = 1, is_empty: bool = False):
        self.value = value
        self.idx = idx
        self.size = size
        self.is_empty = is_empty

    def insert_file(self, file_block: 'DataBlock'):
        """Insert file in empty data-block. Returns new DataBlock created in the place of the old file block"""
        new_empty_block = DataBlock(file_block.value, file_block.idx, file_block.size, True)
        file_block.idx = self.idx
        self.size -= file_block.size
        self.idx += file_block.size
        return new_empty_block

    def __repr__(self):
        value = '.' if self.is_empty else str(self.value)
        return f'{str(value) * self.size} ({self.idx})'

    def __lt__(self, other: 'DataBlock'):
        return self.idx <= other.idx


class Disc:
    def __init__(self, data: str, all_size_one: bool):
        filesystem, file_blocks, empty_blocks = self._get_filesystem(data, all_size_one)
        self.filesystem = filesystem
        self.file_blocks = file_blocks
        self.empty_blocks = empty_blocks

    @property
    def filesystem_checksum(self):
        return sum([
            self._get_file_checksum(block)
            for block in self.file_blocks
        ])

    def print(self, file_per_line: bool = False):
        repr = ''
        for block in sorted(self.filesystem):
            for _ in range(block.size):
                if block.is_empty:
                    repr += '.'
                else:
                    repr += str(block.value)
        print(repr)

        if file_per_line:
            for block in sorted(self.filesystem):
                print(f'{" " * block.idx}{str(block.value) * block.size}')

    @classmethod
    def _get_filesystem(cls, data: str, all_size_one: bool):
        filesystem, file_blocks, empty_blocks, filesystem_idx = cls._initiate_variables()
        for data_idx, size in enumerate(data):
            size = int(size)
            value, is_empty = divmod(data_idx, 2)
            is_empty = bool(is_empty)

            new_blocks = cls._get_new_blocks(all_size_one, filesystem_idx, size, value, is_empty)

            filesystem_idx, filesystem, file_blocks, empty_blocks = cls._update_variables(
                filesystem_idx, size, filesystem, file_blocks, empty_blocks, new_blocks, is_empty,
            )

        return filesystem, file_blocks, empty_blocks

    @classmethod
    def _initiate_variables(cls):
        filesystem: deque[DataBlock] = deque()

        # used as pointers to filesystem entries
        file_blocks: deque[DataBlock] = deque()
        empty_blocks: deque[DataBlock] = deque()

        filesystem_idx = 0
        return filesystem, file_blocks, empty_blocks, filesystem_idx

    @classmethod
    def _get_new_blocks(cls, all_size_one: bool, filesystem_idx: int, size: int, value: int, is_empty: bool):
        if all_size_one:
            new_blocks = [
                    DataBlock(value, filesystem_idx + intern_idx, 1, is_empty)
                    for intern_idx in range(size)
                ]
        else:
            new_blocks = [DataBlock(value, filesystem_idx, size, is_empty)]
        return new_blocks

    @staticmethod
    def _update_variables(
        filesystem_idx: int,
        size: int,
        filesystem: deque[DataBlock],
        file_blocks: deque[DataBlock],
        empty_blocks: deque[DataBlock],
        new_blocks: list[DataBlock],
        is_empty: bool,
    ):
        filesystem_idx += size
        filesystem.extend(new_blocks)
        if is_empty:
            empty_blocks.extend(new_blocks)
        else:
            file_blocks.extendleft(new_blocks)
        return filesystem_idx, filesystem, file_blocks, empty_blocks

    @staticmethod
    def _get_file_checksum(block: DataBlock):
        return sum(
            block.value * (block.idx + internal_idx)
            for internal_idx in range(block.size)
        )


class DiscFragmentator:
    @classmethod
    def fragment_disc(cls, disc: Disc):
        for file_block in disc.file_blocks:
            first_fitting_empty_block = cls._get_first_fitting_empty_block(disc, file_block)
            if first_fitting_empty_block is None:
                continue

            first_fitting_empty_block.insert_file(file_block)

            if first_fitting_empty_block.size == 0:
                cls._remove_obsolete_empty_space(disc, first_fitting_empty_block)

    @classmethod
    def _get_first_fitting_empty_block(cls, disc, file_block):
        return next((
            empty_block
            for empty_block in disc.empty_blocks
            if empty_block.idx < file_block.idx
            and empty_block.size >= file_block.size
        ), None)

    @classmethod
    def _remove_obsolete_empty_space(cls, disc, first_fitting_empty_block):
        disc.empty_blocks.remove(first_fitting_empty_block)
        disc.filesystem.remove(first_fitting_empty_block)


def get_filesystem_checksum(data: str, all_size_one: bool, draw: bool = False):
    data = data.strip()

    disc = Disc(data, all_size_one)
    DiscFragmentator.fragment_disc(disc)
    return disc.filesystem_checksum


def main(data: str):
    filesystem_checksum = get_filesystem_checksum(data, True)
    print(f'Filesystem checksum: {filesystem_checksum}')
    filesystem_checksum_2 = get_filesystem_checksum(data, False)
    print(f'Filesystem checksum 2: {filesystem_checksum_2}')


if __name__ == '__main__':
    with open('09_disk_fragmenter/input', 'r') as f:
        data = f.read()

    main(data)
