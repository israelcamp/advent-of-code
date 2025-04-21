from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

InputType = List[List[str]]


def read_input(file: str) -> InputType:
    lines = Path(file).read_text().splitlines()
    return [list(l) for l in lines]


def reconstruct(data: InputType) -> str:
    return "\n".join(["".join(l) for l in data])


def find_line_coeff(y: int, x: int, y1: int, x1: int) -> tuple[float, float]:
    a = (y - y1) / (x - x1)
    b = y - a * x
    return a, b


def find_distance(y: int, x: int, y1: int, x1: int) -> tuple[int, int]:
    return y - y1, x - x1


def solution_part_one():
    file = "./input.txt"

    data = read_input(file)
    N, M = len(data), len(data[0])
    print(N, M)

    frequency_to_positions = defaultdict(list)
    frequency_to_antinodes = defaultdict(list)
    for i in range(N):
        for j in range(M):
            freq = data[i][j]
            if freq != ".":
                frequency_to_positions[freq].append((i, j))

    for frequency, points in frequency_to_positions.items():

        start = 1
        for position in points[:-1]:
            for other_position in points[start:]:
                x, y = position
                x1, y1 = other_position
                distance_y, distance_x = find_distance(y, x, y1, x1)
                left_point_y = y + distance_y
                left_point_x = x + distance_x
                right_point_y = y1 - distance_y
                right_point_x = x1 - distance_x

                if 0 <= left_point_x < N and 0 <= left_point_y < M:
                    frequency_to_antinodes[frequency].append(
                        (left_point_x, left_point_y)
                    )

                if 0 <= right_point_y < N and 0 <= right_point_x < M:
                    frequency_to_antinodes[frequency].append(
                        (right_point_x, right_point_y)
                    )
            start += 1

    return frequency_to_antinodes


if __name__ == "__main__":
    file = "./input.txt"

    data = read_input(file)
    N, M = len(data), len(data[0])
    print(N, M)

    frequency_to_positions = defaultdict(list)
    frequency_to_antinodes = defaultdict(list)
    for i in range(N):
        for j in range(M):
            freq = data[i][j]
            if freq != ".":
                frequency_to_positions[freq].append((i, j))

    print(frequency_to_positions)
    for frequency, points in frequency_to_positions.items():

        start = 1
        for position in points[:-1]:
            for other_position in points[start:]:
                x, y = position
                x1, y1 = other_position
                distance_y, distance_x = find_distance(y, x, y1, x1)
                frequency_to_antinodes[frequency].append((x, y))
                frequency_to_antinodes[frequency].append((x1, y1))

                add_point = lambda point: 0 <= point[0] < N and 0 <= point[1] < M

                left_point_y = y + distance_y
                left_point_x = x + distance_x
                add_left = add_point((left_point_x, left_point_y))
                while add_left:
                    frequency_to_antinodes[frequency].append(
                        (left_point_x, left_point_y)
                    )
                    left_point_y = left_point_y + distance_y
                    left_point_x = left_point_x + distance_x
                    add_left = add_point((left_point_x, left_point_y))
                    # break

                right_point_y = y1 - distance_y
                right_point_x = x1 - distance_x
                add_right = add_point((right_point_x, right_point_y))
                while add_right:
                    frequency_to_antinodes[frequency].append(
                        (right_point_x, right_point_y)
                    )
                    right_point_y = right_point_y - distance_y
                    right_point_x = right_point_x - distance_x
                    add_right = add_point((right_point_x, right_point_y))
                    # break

                print(position, other_position, distance_x, distance_y)
                # break
            start += 1
        # break

    print("ANTINODES", frequency_to_antinodes)

    print(len(set(sum(frequency_to_antinodes.values(), []))))

    # print(data)
    # print(reconstruct(data))
