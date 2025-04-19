from pathlib import Path


def read_input(file: str):
    data = Path(file).read_text()
    rules, updates = data.split("\n\n")
    return rules.splitlines(), updates.splitlines()


def is_update_valid(rules: list[str], numbers: list[str]) -> bool:
    for i in range(len(numbers) - 1):
        current = numbers[i]
        for j in range(i + 1, len(numbers)):
            next = numbers[j]
            if f"{next}|{current}" in rules:
                return False
    return True


def solution_part_one(rules, updates) -> int:
    result = 0
    for update in updates:
        numbers = update.split(",")
        valid = is_update_valid(rules, numbers)

        if valid:
            result += int(numbers[len(numbers) // 2])

    return result


def swap_invalids(rules: list[str], numbers: list[str]):
    for i in range(len(numbers) - 1):
        current = numbers[i]
        for j in range(i + 1, len(numbers)):
            next = numbers[j]
            if f"{next}|{current}" in rules:
                numbers[i], numbers[j] = numbers[j], numbers[i]
    return numbers


if __name__ == "__main__":
    rules, updates = read_input("input.txt")

    # result_part_one = solution_part_one(rules, updates)
    # print(result_part_one)

    result = 0
    for update in updates:
        numbers = update.split(",")
        valid = is_update_valid(rules, numbers)

        if not valid:
            while not is_update_valid(rules, numbers):
                numbers = swap_invalids(rules, numbers)
            result += int(numbers[len(numbers) // 2])

    print(result)
