from unittest import TestCase

from index03 import MemoryParser


class TestMemoryParser(TestCase):
    def test_get_sum(self):
        input = r'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'
        parser = MemoryParser()
        result = parser.get_sum(input)
        self.assertEqual(result, 161)

    def test_get_sum_with_disablers(self):
        input = (
            'mul(1,2)don\'t()mul(2,3)don\'t()mul(3,4)do()mul(4,5)do()mul(5,6)don\'t()mul(6,7)'
            'do()mul(7,8)don\'t()mul(8,9)'
        )
        parser = MemoryParser()
        result = parser.get_sum_with_disablers(input)
        self.assertEqual(result, 1*2 + 4*5 + 5*6 + 7*8)
