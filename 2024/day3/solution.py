from pathlib import Path
import re


def read_input(file: str) -> str:
    return Path(file).read_text()


def find_mul_operation(data: str) -> list[str]:
    pattern = re.compile(r"mul\([0-9]{1,3},[0-9]{1,3}\)")
    return pattern.findall(data)


def perform_mul_operation(mul_string: str) -> int:
    left, right = [int(x) for x in re.findall(r"[0-9]{1,3}", mul_string)]
    return left * right


def part_one_solution(data: str) -> int:
    operations = find_mul_operation(data=data)

    result = 0
    for mulop in operations:
        mul_value = perform_mul_operation(mulop)

        result += mul_value
    return result


if __name__ == "__main__":

    data = read_input("input.txt")

    # operations = find_mul_operation(data=data)

    current_index = 0
    parts: list[str] = []

    current_end = len(data)
    for match in reversed(list(re.finditer(r"don't\(\)|do\(\)", data))):
        match_string = match.group(0)
        start, end = match.span(0)

        parts.append(data[start:current_end])

        current_end = start

    parts.append(data[0:current_end])

    do_parts = [p for p in parts if not p.startswith("don't()")]
    print(len(parts), len(do_parts))

    result = 0
    for part in do_parts:
        operations = find_mul_operation(part)
        result += sum([perform_mul_operation(op) for op in operations])
    print(result)
