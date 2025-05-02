from pathlib import Path


def read_input(file: str):
    data = Path(file).read_text()
    lines = data.splitlines()
    positions = []
    for line in lines:
        col, row = [int(x) for x in line.split(",")]
        positions.append((row, col))
    return positions


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
    bytes_positions = bytes_positions[:FALLEN_BYTES]

    fallen_grid = []
    for i in range(N):
        row = []
        for j in range(N):
            if (i, j) in bytes_positions:
                row.append("#")
            else:
                row.append(".")
        fallen_grid.append(row)

    Path("grid.txt").write_text("\n".join("".join(row) for row in fallen_grid))

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

                if (next_row, next_col) in bytes_positions:
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

                if (next_row, next_col) == (0, 0):
                    SOLUTION_SCORE = next_score
                    SOLUTION_STEP = next_step
                    continue

                next_steps.append(next_step)

        current_steps = next_steps

    print(SOLUTION_SCORE)
