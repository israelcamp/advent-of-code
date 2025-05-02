from pathlib import Path


def read_input(file: str):
    data = Path(file).read_text()
    lines = data.splitlines()
    positions = []
    for line in lines:
        col, row = [int(x) for x in line.split(",")]
        positions.append((row, col))
    return positions


def solution_part_one(fallen_bytes: list[tuple[int, int]], N, target_row: int, target_col: int) -> int:
    SOLUTION_SCORE = 1_000_000
    SOLUTION_STEP = None

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    memo = {}
    start_step = {
        "row": N-1, "col": N-1, "next": None, "score": 0
    }

    current_steps = [start_step]

    while len(current_steps) > 0:
        next_steps = []
        for step in current_steps:
            for drow, dcol in directions:
                next_row, next_col = step["row"] + drow, step["col"] + dcol

                if next_row < 0 or next_row >= N or next_col < 0 or next_col >= N:
                    continue

                if (next_row, next_col) in fallen_bytes:
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

                if (next_row, next_col) == (target_row, target_col):
                    SOLUTION_SCORE = next_score
                    SOLUTION_STEP = next_step
                    continue

                next_steps.append(next_step)

        current_steps = next_steps

    return SOLUTION_STEP


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    file = f"{filename}.txt"

    if filename.startswith("sample"):
        N, FALLEN_BYTES = 7, 12
    else:
        N = 71
        FALLEN_BYTES = 1024

    SOLUTION_SCORE = 1_000_000
    SOLUTION_STEP = None

    bytes_positions = read_input(file)
    fallen_bytes_grid = bytes_positions[:FALLEN_BYTES]

    solution_step = solution_part_one(fallen_bytes_grid, N, 0, 0)
    solution_potisions = []
    step = solution_step
    while step is not None:
        solution_potisions.append((step["row"], step["col"]))
        step = step["next"]

    while FALLEN_BYTES < len(bytes_positions):
        next_fallen_byte = FALLEN_BYTES + 1
        if bytes_positions[next_fallen_byte] not in solution_potisions:
            FALLEN_BYTES += 1
            continue

        solution_step = solution_part_one(bytes_positions[:next_fallen_byte+1], N, 0, 0)

        if solution_step is None:
            print("STOP", bytes_positions[next_fallen_byte])
            break

        solution_potisions = []
        step = solution_step
        while step is not None:
            solution_potisions.append((step["row"], step["col"]))
            step = step["next"]
