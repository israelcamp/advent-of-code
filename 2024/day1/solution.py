from pathlib import Path
from collections import Counter


def read_input(file_path: str) -> tuple[list[int], list[int]]:
    text = Path(file_path).read_text()
    lines = text.splitlines()
    left_list, right_list = [], []
    for line in lines:
        left, right = line.strip().split()
        left_list.append(int(left))
        right_list.append(int(right))

    assert len(left_list) == len(right_list), "Lists must be of equal length"
    return left_list, right_list


def distances_part_one(left_list: list[int], right_list: list[int]) -> int:
    left_list.sort()
    right_list.sort()

    total_distance = 0
    for left, right in zip(left_list, right_list):
        total_distance += abs(left - right)

    return total_distance


if __name__ == "__main__":
    left_list, right_list = read_input("day1.txt")

    left_counter = Counter(left_list)
    right_counter = Counter(right_list)

    total_distance = 0
    for key, value in left_counter.items():
        distance = key * value * right_counter.get(key, 0)
        total_distance += distance

    print(total_distance)
