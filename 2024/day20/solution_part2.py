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


def find_next_points(board, start_row: int, start_col: int, current_row: int, current_col: int, current_step:int, max_step: int, start_score: int, min_score: int, N: int, visited:list, directions, memo: dict, memo_cheats: set):
    
    if current_step > max_step: ## TODO: maybe I will be off by one
        return 0

    visited.append((current_row, current_col))

    paths = 0
    for drow, dcol in directions:
        next_row, next_col = current_row + drow, current_col + dcol

        if next_row < 0 or next_row >= N or next_col < 0 or next_col >= N:
                continue
        
        if (next_row, next_col) in visited:
            continue

        next_symbol = board[next_row][next_col]
        if next_symbol != "#":
            next_score = memo[(next_row, next_col)]
            time_saved = start_score - next_score - current_step
            if time_saved >= min_score:
                memo_cheats.add((start_row, start_col, next_row, next_col))
                paths += 1

        paths += find_next_points(
            board=board,
            start_row=start_row,
            start_col=start_col,
            current_row=next_row,
            current_col=next_col,
            current_step=current_step + 1,
            max_step=max_step,
            start_score=start_score,
            min_score=min_score,
            N=N,
            directions=directions,
            visited=visited.copy(),
            memo=memo,
            memo_cheats=memo_cheats
        )

    return paths


def manhatan_distance(x: int, y: int, x1: int, y1: int) -> int:
    return abs(x - x1) + abs(y - y1)


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

    cheat_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    min_cheat = int(sys.argv[2])

    final_score = solution_step["score"]

    step = solution_step
    matches = set()
    memo_cheats = set()
    while step is not None:
        row, col = step["row"], step["col"]

        if step["score"] < min_cheat:
            step = step["next"]
            continue

        for drow, dcol in cheat_directions:
            next_row, next_col = row + drow, col + dcol

            if next_row < 0 or next_row >= N or next_col < 0 or next_col >= N:
                continue

            if board[next_row][next_col] != "#": ## only starts right before walls
                continue

            cheat_row, cheat_col = next_row + drow, next_col + dcol
            if next_row < 0 or next_row >= N or next_col < 0 or next_col >= N:
                continue

            possible_ends = [
                (r, c, s) for (r,c), s in memo.items() if manhatan_distance(r, c, cheat_row, cheat_col) <= 18
            ]
            for r, c, s in possible_ends:
                time_saved = step["score"] - s - manhatan_distance(r, c, row, col)
                if time_saved >= min_cheat:
                    memo_cheats.add((row, col, r, c))
        
        step = step["next"]

    # print(memo_cheats)
    print(len(memo_cheats))
