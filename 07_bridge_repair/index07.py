from itertools import product
from typing import Callable


Operator = Callable[[int, int], int]


class Equation:
    OPERATORS: list[Operator] = [
        lambda x, y: x + y,
        lambda x, y: x * y,
    ]

    def __init__(self, equation):
        value, numbers = equation.split(': ')
        self.value = int(value)
        self.numbers = list(map(int, numbers.split(' ')))
        self.operators = self._get_correct_operators()

    def _get_correct_operators(self):
        required_operators_count = self._get_required_operators_count()
        possible_combinations = self._get_possible_operators_combinations(required_operators_count)
        return next((
            combination
            for combination in possible_combinations
            if self._is_combination_correct(combination)
        ), None)

    def _get_required_operators_count(self):
        return len(self.numbers) - 1

    @classmethod
    def _get_possible_operators_combinations(cls, required_operators_count: int):
        return product(cls.OPERATORS, repeat=required_operators_count)

    def _is_combination_correct(self, combination: tuple[Operator, ...]):
        result = self.numbers[0]
        for operator, number in zip(combination, self.numbers[1:]):
            result = operator(result, number)
        return result == self.value


class Equation2(Equation):
    OPERATORS: list[Operator] = [
        lambda x, y: x + y,
        lambda x, y: x * y,
        lambda x, y: int(f'{x}{y}'),
    ]


def set_up(data: str):
    equations = [
        Equation(equation)
        for equation in data.split('\n')
        if equation != ''
    ]
    return equations


def get_total_calibration_result(equations: list[Equation]):
    return sum(equation.value for equation in equations if equation.operators is not None)


def get_total_calibration_result_2(data: str, eq_from_part_1: list[Equation]):
    done_values = [
        equation.value
        for equation in eq_from_part_1
        if equation.operators is not None
    ]
    equations = [
        Equation2(equation)
        for equation in data.split('\n')
        if equation != '' and int(equation.split(': ')[0]) not in done_values
    ]
    return sum(done_values) + sum(equation.value for equation in equations if equation.operators is not None)


def main(data: str):
    eq_from_part_1 = set_up(data)
    total_calibration_result = get_total_calibration_result(eq_from_part_1)
    total_calibration_result_2 = get_total_calibration_result_2(data, eq_from_part_1)
    print(f'Total calibration result: {total_calibration_result}')
    print(f'Total calibration result 2: {total_calibration_result_2}')


if __name__ == '__main__':
    with open('07_bridge_repair/input', 'r') as f:
        data = f.read()

    main(data)
