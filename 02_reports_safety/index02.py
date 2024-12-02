def get_levels(report: str) -> list[int]:
    return list(map(int, report.split(' ')))


def is_increasing(levels: list[int]) -> bool:
    return all(x < y for x, y in zip(levels, levels[1:]))


def is_decreasing(levels: list[int]) -> bool:
    return all(x > y for x, y in zip(levels, levels[1:]))


def is_spacing_correct(levels: list[int], min: int, max: int) -> bool:
    return all(abs(x - y) in range(min, max + 1) for x, y in zip(levels, levels[1:]))


def get_is_report_safe(levels: list[int]) -> bool:
    return (
        (is_increasing(levels) or is_decreasing(levels))
        and is_spacing_correct(levels, 1, 3)
    )


def get_safe_reports_count(reports: list[str]) -> int:
    return len([
        report
        for report in reports
        if get_is_report_safe(get_levels(report))
    ])


def get_levels_without_index(levels: list[int], index: int) -> list[int]:
    return levels[:index] + levels[index + 1:]


def get_is_report_weak_safe(report: str) -> bool:
    levels = get_levels(report)
    if get_is_report_safe(levels):
        return True

    return any(
        get_is_report_safe(get_levels_without_index(levels, index))
        for index in range(len(levels))
    )


def get_weak_safe_reports_count(reports: list[str]) -> int:
    return len([
        report
        for report in reports
        if get_is_report_weak_safe(report)
    ])


if __name__ == '__main__':
    with open('02_reports_safety/input', 'r') as f:
        reports = f.readlines()
    safe_reports_count = get_safe_reports_count(reports)
    weak_safe_reports_count = get_weak_safe_reports_count(reports)
    print(f'Safe reports count: {safe_reports_count}')
    print(f'Weak safe reports count: {weak_safe_reports_count}')
