from pathlib import Path


def read_input(file: str):
    data = Path(file).read_text().splitlines()
    return [list(l) for l in data]


def solve_race(
    walls: list[tuple[int, int]],
    N,
    start_row: int,
    start_col: int,
    target_row: int,
    target_col: int,
    memo: dict,
):
    SOLUTION_SCORE = 1_000_000
    SOLUTION_STEP = None

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    start_step = {"row": target_row, "col": target_col, "next": None, "score": 0}

    current_steps = [start_step]

    while len(current_steps) > 0:
        next_steps = []
        for step in current_steps:
            for drow, dcol in directions:
                next_row, next_col = step["row"] + drow, step["col"] + dcol

                if next_row < 0 or next_row >= N or next_col < 0 or next_col >= N:
                    continue

                if (next_row, next_col) in walls:
                    continue

                next_score = step["score"] + 1

                memo_score = memo.get((next_row, next_col), None)
                if memo_score is not None and next_score >= memo_score:
                    continue

                if next_score >= SOLUTION_SCORE:
                    continue

                memo[(next_row, next_col)] = next_score
                next_step = dict(
                    row=next_row, col=next_col, next=step, score=next_score
                )

                if (next_row, next_col) == (start_row, start_col):
                    SOLUTION_SCORE = next_score
                    SOLUTION_STEP = next_step
                    continue

                next_steps.append(next_step)

        current_steps = next_steps

    return SOLUTION_STEP


if __name__ == "__main__":
    import sys

    _filename = sys.argv[1]
    filename = f"{_filename}.txt"

    board = read_input(filename)
    N = len(board)

    walls = []
    for i in range(N):
        for j in range(N):
            symbol = board[i][j]
            if symbol == "S":
                start_row, start_col = i, j
            if symbol == "E":
                target_row, target_col = i, j
            if symbol == "#":
                walls.append((i, j))

    memo = {}
    memo[(target_row, target_col)] = 0
    solution_step = solve_race(
        walls, N, start_row, start_col, target_row, target_col, memo
    )

    cheat_directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
    min_cheat = int(sys.argv[2])

    final_score = solution_step["score"]

    step = solution_step
    matches = set()
    while step is not None:
        row, col = step["row"], step["col"]

        if step["score"] < min_cheat:
            step = step["next"]
            continue

        for drow, dcol in cheat_directions:
            next_row, next_col = row + drow, col + dcol

            if next_row < 0 or next_row >= N or next_col < 0 or next_col >= N:
                continue

            if board[next_row][next_col] == "#":
                continue

            if board[row + drow // 2][col + dcol // 2] != "#":
                continue

            if (next_row, next_col) in memo:
                next_score = memo[(next_row, next_col)]

            time_saved = step["score"] - next_score - 2 ## 2 because it takes 2 picoseconds to get there
            if next_score <= step["score"] and time_saved >= min_cheat:
                matches.add((row, col, next_row, next_col))

        step = step["next"]

    print(len(matches))
