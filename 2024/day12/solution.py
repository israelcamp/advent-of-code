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


def calculate_connection_bulk(
    data,
    row: int,
    col: int,
    area: int,
    plant: str,
    N: int,
    M: int,
    done: list,
    posd: dict,
    key: str,
):
    if (row, col) in done:
        return 0, 0

    if key is None:
        key = (row, col)
        posd[key] = {}

    done.append((row, col))

    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    plant_dict = {d: False for d in directions}

    perimeter = 0
    for di, dj in directions:
        next_row, next_col = row + di, col + dj
        if next_row < 0 or next_row >= N or next_col < 0 or next_col >= M:
            perimeter += 1
            continue

        connected = data[next_row][next_col] == plant
        plant_dict[(di, dj)] = connected

        if not connected:
            perimeter += 1
        elif (next_row, next_col) in done:
            continue
        else:
            area_from_others, perimeter_from_others = calculate_connection_bulk(
                data, next_row, next_col, area + 1, plant, N, M, done, posd, key
            )
            area = area_from_others
            perimeter += perimeter_from_others

    posd[key][(row, col)] = plant_dict

    return area, perimeter


if __name__ == "__main__":
    file = "./input.txt"
    data = read_input(file)
    N, M = len(data), len(data[0])

    result = 0
    done = []
    posd = {}
    for i in range(N):
        for j in range(M):
            if (i, j) in done:
                continue
            area, perimeter = calculate_connection_bulk(
                data, i, j, 1, data[i][j], N, M, done, posd, None
            )
            result += area * perimeter
        #     break
        # break

    print(result)

    dirs = [
        [(-1, 0), (0, 1)],
        [(0, -1), (1, 0)],
        [(0, 1), (1, 0)],
        [(1, 0), (0, 1)],
    ]  # WILL CHECK UP
    side_per_region = {}
    result = 0
    for start, region in posd.items():

        keys = list(region.keys())
        keys = sorted(keys, key=lambda x: N * x[0] + x[1])
        accounted_for = []
        sides = 0
        side_per_region[start] = 0

        for point in keys:
            for current_direction, opposite_direction in dirs:
                point_dirs = region[point]

                if (point + current_direction) in accounted_for:
                    continue

                if point_dirs[current_direction] is False:
                    row, col = point
                    side_per_region[start] += 1
                    distance = 1
                    accounted_for.append((row, col) + current_direction)
                    while True:
                        next_row = row + opposite_direction[0] * distance
                        next_col = col + opposite_direction[1] * distance
                        if (
                            next_row < 0
                            or next_row >= N
                            or next_col < 0
                            or next_col >= M
                        ):
                            break
                        if (next_row, next_col) not in keys:
                            break
                        next_point_dirs = region[(next_row, next_col)]

                        if next_point_dirs[current_direction] is True:
                            accounted_for.append(
                                (next_row, next_col) + current_direction
                            )
                            break

                        distance += 1
                        accounted_for.append((next_row, next_col) + current_direction)

        result += len(region) * side_per_region[start]

    print(result)
