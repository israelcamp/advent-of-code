from pathlib import Path
from collections import namedtuple


def read_input(file: str) -> list[list[str]]:
    data = Path(file).read_text()
    lines = data.splitlines()
    return [list(l) for l in lines]


def calculate_connection(
    data, row: int, col: int, area: int, plant: str, N: int, M: int, done: list
):
    if (row, col) in done:
        return 0, 0

    done.append((row, col))

    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    perimeter = 0
    for di, dj in directions:
        next_row, next_col = row + di, col + dj
        if next_row < 0 or next_row >= N or next_col < 0 or next_col >= M:
            perimeter += 1
        elif data[next_row][next_col] != plant:
            perimeter += 1
        elif (next_row, next_col) in done:
            continue
        else:
            area_from_others, perimeter_from_others = calculate_connection(
                data, next_row, next_col, area + 1, plant, N, M, done
            )
            area = area_from_others
            perimeter += perimeter_from_others

    return area, perimeter


if __name__ == "__main__":
    file = "./sample3.txt"
    data = read_input(file)
    N, M = len(data), len(data[0])

    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]

    result = 0
    done = []
    for i in range(N):
        for j in range(M):
            if (i, j) in done:
                continue
            area, perimeter = calculate_connection(
                data, i, j, 1, data[i][j], N, M, done
            )
            result += area * perimeter

    print(result)
