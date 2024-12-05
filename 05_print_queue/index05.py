class PageNumber:
    def __init__(self, value: int):
        self.number = value
        self.pages_before: list[int] = []
        self.pages_after: list[int] = []

    def add_rule(self, pre_page: int, post_page: int):
        """Rule have form of 'A|B' where A and B are page numbers"""
        if pre_page == self.number:
            self.pages_after.append(post_page)
        self.pages_before.append(pre_page)

    def get_is_well_placed(self, pageOrder: list[int]):
        wrong_page, _ = self._get_wrongly_placed_page(pageOrder)
        return wrong_page is None

    def get_wrong_rule(self, pageOrder: list[int]):
        wrong_page, is_after = self._get_wrongly_placed_page(pageOrder)

        if wrong_page is None:
            return None

        if is_after:
            return self.number, wrong_page
        return wrong_page, self.number

    def _get_wrongly_placed_page(self, pageOrder: list[int]):
        myIdx = pageOrder.index(self.number)
        wrong_page_before = self._get_wrongly_placed_page_before(pageOrder, myIdx)
        if wrong_page_before is not None:
            return wrong_page_before, False
        wrong_page_after = self._get_wrongly_placed_page_after(pageOrder, myIdx)
        return wrong_page_after, True

    def _get_wrongly_placed_page_before(self, pageOrder: list[int], myIdx: int):
        if myIdx == 0:
            return None
        return next(
            (
                pageOrder[idx]
                for idx in range(myIdx)
                if pageOrder[idx] in self.pages_after
            ),
            None,
        )

    def _get_wrongly_placed_page_after(self, pageOrder: list[int], myIdx: int):
        if myIdx == len(pageOrder) - 1:
            return None
        return next(
            (
                pageOrder[idx]
                for idx in range(myIdx + 1, len(pageOrder))
                if pageOrder[idx] in self.pages_before
            ),
            None,
        )

    def __repr__(self):
        return f'PageNumber(number={self.number}, pages_before={self.pages_before}, pages_after={self.pages_after})'


class PageNumberDict:
    def __init__(self):
        self.numbers: dict[int, PageNumber] = {}

    def parse_rule_set(self, rule_set: str):
        for rule in rule_set.split('\n'):
            self._parse_rule(rule)

    def _parse_rule(self, rule):
        pre_page, post_page = rule.split('|')
        pre_page = int(pre_page.strip())
        post_page = int(post_page.strip())
        if pre_page not in self.numbers:
            self.numbers[pre_page] = PageNumber(int(pre_page))
        if post_page not in self.numbers:
            self.numbers[post_page] = PageNumber(int(post_page))
        self.numbers[pre_page].add_rule(pre_page, post_page)
        self.numbers[post_page].add_rule(pre_page, post_page)


class Update:
    def __init__(self, page_order: list[int], numbers_dict: PageNumberDict):
        self.page_order = page_order
        self.is_correct = self.get_is_correct(page_order, numbers_dict)

    def get_middle_page_number(self):
        middle_idx = len(self.page_order) // 2
        return self.page_order[middle_idx]

    def get_correct_order(self, numbers_dict: PageNumberDict):
        return UpdateFixingService.get_fixed_page_order(self.page_order, numbers_dict)

    @staticmethod
    def get_is_correct(pageOrder: list[int], numbers_dict: PageNumberDict):
        return all(
            numbers_dict.numbers[page].get_is_well_placed(pageOrder)
            for page in pageOrder
        )


class UpdateSet:
    def __init__(self):
        self.updates: list[Update] = []

    def parse_update_set(self, update_set: str, numbers_dict: PageNumberDict):
        for update in update_set.split('\n'):
            self._parse_update(update, numbers_dict)

    def _parse_update(self, update: str, numbers_dict: PageNumberDict):
        pageOrder = [int(page) for page in update.split(',')]
        self.updates.append(Update(pageOrder, numbers_dict))


class UpdateSetAggregator:
    @staticmethod
    def get_sum_of_middle_page_number(update_set: UpdateSet):
        return sum(
            update.get_middle_page_number()
            for update in update_set.updates
            if update.is_correct
        )

    @staticmethod
    def get_sum_of_middle_page_number_for_fixed_wrong_updates(update_set: UpdateSet, numbers_dict: PageNumberDict):
        incorrect_updates = [
            update
            for update in update_set.updates
            if not update.is_correct
        ]

        for update in incorrect_updates:
            update.get_correct_order(numbers_dict)

        return sum(
            update.get_middle_page_number()
            for update in incorrect_updates
        )


class UpdateFixingService:
    @classmethod
    def get_fixed_page_order(cls, page_order: list[int], numbers_dict: PageNumberDict):
        while True:
            wrong_rule = cls._get_wrong_rule(page_order, numbers_dict)
            if wrong_rule is None:
                break
            cls._swap_pages_from_rule(page_order, wrong_rule)
        return page_order

    @staticmethod
    def _swap_pages_from_rule(page_order: list[int], rule: tuple[int, int]):
        first_idx = page_order.index(rule[0])
        second_idx = page_order.index(rule[1])
        temp = page_order[first_idx]
        page_order[first_idx] = page_order[second_idx]
        page_order[second_idx] = temp

    @staticmethod
    def _get_wrong_rule(page_order: list[int], numbers_dict: PageNumberDict):
        return next((
            rule
            for page in page_order
            if (rule := numbers_dict.numbers[page].get_wrong_rule(page_order)) is not None
        ), None)


def set_up(data: str):
    rules, updates = data.split('\n\n')

    page_number_set = PageNumberDict()
    page_number_set.parse_rule_set(rules.strip())

    update_set = UpdateSet()
    update_set.parse_update_set(updates.strip(), page_number_set)
    return page_number_set, update_set


def get_average_middle_page_number(page_number_set: PageNumberDict, update_set: UpdateSet):
    return UpdateSetAggregator.get_sum_of_middle_page_number(update_set)


def get_average_middle_page_number_for_fixed_wrong_updates(page_number_set: PageNumberDict, update_set: UpdateSet):
    return UpdateSetAggregator.get_sum_of_middle_page_number_for_fixed_wrong_updates(update_set, page_number_set)


def main(data: str):
    page_number_set, update_set = set_up(data)

    average_middle_page_number = get_average_middle_page_number(page_number_set, update_set)
    average_middle_page_number_of_fixed = get_average_middle_page_number_for_fixed_wrong_updates(
        page_number_set, update_set,
    )

    print(f'Average middle page number: {average_middle_page_number}')
    print(f'Average middle page number of fixed wrong updates: {average_middle_page_number_of_fixed}')


if __name__ == '__main__':
    with open('05_print_queue/input', 'r') as f:
        data = f.read()

    main(data)
