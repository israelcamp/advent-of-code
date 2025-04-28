from pathlib import Path
import sys

sys.setrecursionlimit(10000)


START = "S"
END = "E"
WALL = "#"
FREE = "."
INF_SCORE = 1_000_000_00


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


class Step:
    def __init__(self, row: int, col: int, drow: int, dcol: int, previous=None):
        self.row = row
        self.col = col
        self.drow = drow
        self.dcol = dcol
        self.previous = previous


RESULTS: list[int] = []


def calculate_step_score(step: Step, maze, memo: dict) -> int:

    # _memo = memo.get((step.row, step.col, step.drow, step.dcol), None)
    # if _memo is None:
    #     memo[(step.row, step.col, step.drow, step.dcol)] = []
    # return _memo

    where_am_i = maze[step.row][step.col]
    if where_am_i == WALL:
        return INF_SCORE
    if where_am_i == END:
        return 0

    possible_directions = find_next_directions((step.drow, step.dcol))

    where_can_i_go = [
        (step.row + drow, step.col + dcol, drow, dcol)
        for (drow, dcol) in possible_directions
    ]
    previous_step: Step = step.previous
    previous_len: int = 0
    while previous_step is not None:
        previous_point = (
            previous_step.row,
            previous_step.col,
            previous_step.drow,
            previous_step.dcol,
        )
        if previous_point in where_can_i_go:
            where_can_i_go.remove(previous_point)

        previous_len += 1
        previous_step = previous_step.previous

    if not len(where_can_i_go):
        return INF_SCORE

    results = []
    for row, col, drow, dcol in where_can_i_go:
        memo_key = (
            step.row,
            step.col,
            step.drow,
            step.dcol,
            row,
            col,
            drow,
            dcol,
            previous_len,
        )
        memo_value = memo.get(memo_key, None)
        if memo_value is not None:
            results.append(memo_value)
            continue

        step_score = calculate_step_score(
            Step(row, col, drow, dcol, previous=step), maze, memo
        )
        score = 1 + step_score
        if (drow, dcol) != (step.drow, step.dcol):
            score += 1000

        memo[memo_key] = score

        results.append(score)
    min_score = min(results)

    # print("THIS STEP", step.row, step.col, step.drow, step.dcol, "SCORE", min_score)
    return min_score


if __name__ == "__main__":
    file = "./sample2.txt"
    maze = read_input(file)

    print(draw_maze(maze))

    ## I NEED TO SAVE THE DIRECTION I ARRIVED

    start_row, start_col = find_start(maze)
    start_direction = (0, -1)
    # row, col = start_row, start_col + 1

    start_step = Step(
        row=start_row,
        col=start_col,
        drow=start_direction[0],
        dcol=start_direction[1],
        previous=None,
    )
    memo = {}
    result = calculate_step_score(start_step, maze, memo)
    print(result)

    # for k, v in memo.items():
    #     if len(set(v)) > 1:
    #         print(k, v)
