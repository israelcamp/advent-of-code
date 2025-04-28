from pathlib import Path
import sys

sys.setrecursionlimit(2000)


START = "S"
END = "E"
WALL = "#"
FREE = "."


def read_input(file: str) -> list[list[str]]:
    data = Path(file).read_text().splitlines()
    return [list(l) for l in data]


def draw_maze(maze: list[list[str]]) -> str:
    return "\n".join(["".join(row) for row in maze])


def rotate_vector(x: int, y: int, angle: int) -> tuple[int, int]:
    if angle == 90:
        return (y, -x)
    if angle == -90:
        return (-y, x)

    return -1, -1


def find_start(maze) -> tuple[int, int]:
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == START:
                return i, j
    return -1, -1


def find_next_directions(current_direction: tuple[int, int]):
    clockwise_dcol, clockwise_drow = rotate_vector(
        current_direction[1], current_direction[0], 90
    )
    anticlockwise_dcol, anticlockwise_drow = rotate_vector(
        current_direction[1], current_direction[0], -90
    )
    return [
        current_direction,
        (clockwise_drow, clockwise_dcol),
        (anticlockwise_drow, anticlockwise_dcol),
    ]


def find_min_path(
    row: int,
    col: int,
    maze,
    current_direction: tuple[int, int],
    visited: list,
    memo: dict,
) -> int:
    # i am at (row, col) = (y, x) arriving coming from the current_direction

    # will save the places visited
    forward_visited = visited.copy()
    forward_visited.append((row, col, *current_direction))
    # if len(forward_visited) == 5:
    #     return 1

    # if this position and direction already exists
    _memo = memo.get((row, col, *current_direction), None)
    if _memo is not None:
        return _memo

    # those are the directions that i can keep moving
    next_directions = find_next_directions(current_direction)

    # this will save the result from each direction i can go
    results = []

    # for each direction i can go:
    for drow, dcol in next_directions:

        next_row, next_col = row + drow, col + dcol
        next_place = maze[next_row][next_col]
        if (
            next_place in (WALL, START)
            or (next_row, next_col, drow, dcol) in forward_visited
        ):
            path_score = 1_000_000_000
        elif next_place == END:
            path_score = 0
        elif next_place == FREE:
            path_score = find_min_path(
                next_row, next_col, maze, (drow, dcol), forward_visited, memo
            )

        score = 1
        if (drow, dcol) != current_direction:
            score += 1000

        r = score + path_score
        results.append(r)
        break

    result = min(results)

    memo[(row, col, *current_direction)] = result

    return result


if __name__ == "__main__":
    file = "./sample.txt"
    maze = read_input(file)

    print(draw_maze(maze))

    start_row, start_col = find_start(maze)
    start_direction = (0, -1)
    row, col = start_row, start_col + 1

    visited = []
    memo = {}
    result = find_min_path(start_row, start_col, maze, start_direction, visited, memo)

    print(result)
