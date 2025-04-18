from pathlib import Path


def read_file(file_path: str) -> list[list[int]]:
    text = Path(file_path).read_text()
    rows = []
    for line in text.splitlines():
        rows.append([int(c) for c in line.split()])
    return rows


def is_report_safe(report: list[int]) -> bool:
    min_gap, max_gap = 1, 3
    sign = None

    left = report[0]
    for right in report[1:]:
        gap = left - right
        gap_abs = abs(gap)

        if gap_abs < min_gap or gap_abs > max_gap:
            return False

        current_sign = int(gap / gap_abs)
        if sign is None:
            sign = current_sign

        if current_sign != sign:
            return False

        left = right

    return True


## dummy solution for part 2
def is_there_safe_subset_from_report(report: list[int]) -> bool:
    for index in range(len(report)):
        new_report = report.copy()
        new_report.pop(index)

        assert len(new_report) == len(report) - 1

        if is_report_safe(new_report):
            return True

    return False


if __name__ == "__main__":

    data = read_file("./input.txt")

    count = 0
    count_part2 = 0
    for report in data:
        safe = is_report_safe(report=report)

        if not safe:  ## code for part 2
            safe = is_there_safe_subset_from_report(report)

        count += safe

    print(count)
