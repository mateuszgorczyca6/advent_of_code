import re


class MemoryParser:
    def get_sum(self, memory: str) -> int:
        number_pairs = self._parse_memory(memory)
        return sum([int(x) * int(y) for x, y in number_pairs])

    def get_sum_with_disablers(self, memory: str) -> int:
        modified_memory = ''.join(memory.split('\n')) + 'do()'
        filtered_memory = re.sub(r'don\'t\(\).*?do\(\)', 'don\'t()do()', modified_memory)
        return self.get_sum(filtered_memory)

    def _parse_memory(self, memory: str) -> list[str]:
        return re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', memory)


if __name__ == '__main__':
    with open('03_mul/input', 'r') as f:
        data = f.read()

    mul_sum = MemoryParser().get_sum(data)
    mul_sum_with_disablers = MemoryParser().get_sum_with_disablers(data)
    print(f'Mul sum: {mul_sum}')
    print(f'Mul sum with disablers: {mul_sum_with_disablers}')
