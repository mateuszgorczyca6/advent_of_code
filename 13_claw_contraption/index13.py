import re


class ClawMachine:
    def __init__(self, button_A: tuple[int, int], button_B: tuple[int, int], prize: tuple[int, int]):
        self.button_A = button_A
        self.button_B = button_B
        self.prize = prize

    def get_fewest_token_win(self):
        """Rules:
        * max presses of A = 100
        * max presses of B = 100
        * A cost 3 tokens
        * B cost 1 token"""
        solutions_prices = [
            num_a * 3 + num_b
            for num_a in range(101)
            for num_b in range(101)
            if (
                num_a * self.button_A[0] + num_b * self.button_B[0] == self.prize[0]
                and num_a * self.button_A[1] + num_b * self.button_B[1] == self.prize[1]
            )
        ]
        return min(solutions_prices) if solutions_prices else None

    def get_fewest_token_win_2(self):
        """Explanation in README at the bottom."""
        b_presses = (
            (self.prize[0] * self.button_A[1] - self.prize[1] * self.button_A[0])
            / (self.button_B[0] * self.button_A[1] - self.button_B[1] * self.button_A[0])
        )
        if not b_presses.is_integer():
            return None

        a_presses = (self.prize[0] - b_presses * self.button_B[0]) / self.button_A[0]
        if not a_presses.is_integer():
            return None

        return int(a_presses) * 3 + int(b_presses)

    def __repr__(self):
        return f'ClawMachine(A={self.button_A}, B={self.button_B}, Prize={self.prize})'


def set_up(raw_data: str):
    return raw_data


def get_num_of_tokens(data: str):
    machines = set()
    for machine_setup in data.split('\n\n'):
        button_A_setup, button_B_setup, prize_setup = machine_setup.split('\n')
        ax, ay = re.match(r'Button A: X\+(\d+), Y\+(\d+)', button_A_setup).groups()  # type: ignore
        bx, by = re.match(r'Button B: X\+(\d+), Y\+(\d+)', button_B_setup).groups()  # type: ignore
        px, py = re.match(r'Prize: X=(\d+), Y=(\d+)', prize_setup).groups()  # type: ignore
        machines.add(ClawMachine((int(ax), int(ay)), (int(bx), int(by)), (int(px), int(py))))

    return sum(
        fewest_token_win
        for machine in machines
        if (fewest_token_win := machine.get_fewest_token_win()) is not None
    )


def get_num_of_tokens_2(data: str):
    machines = set()
    for machine_setup in data.split('\n\n'):
        button_A_setup, button_B_setup, prize_setup = machine_setup.split('\n')
        ax, ay = re.match(r'Button A: X\+(\d+), Y\+(\d+)', button_A_setup).groups()  # type: ignore
        bx, by = re.match(r'Button B: X\+(\d+), Y\+(\d+)', button_B_setup).groups()  # type: ignore
        px, py = re.match(r'Prize: X=(\d+), Y=(\d+)', prize_setup).groups()  # type: ignore
        machines.add(
            ClawMachine((int(ax), int(ay)), (int(bx), int(by)), (int(px) + 10000000000000, int(py) + 10000000000000)),
        )

    return sum(
        fewest_token_win
        for machine in machines
        if (fewest_token_win := machine.get_fewest_token_win_2()) is not None
    )


def main(data: str):
    data = set_up(data.strip())
    num_of_tokens = get_num_of_tokens(data)
    num_of_tokens_2 = get_num_of_tokens_2(data)
    print(f'Nuber of tokens: {num_of_tokens}')
    print(f'Nuber of tokens 2: {num_of_tokens_2}')


if __name__ == '__main__':
    with open('13_claw_contraption/input', 'r') as f:
        data = f.read()

    main(data)
