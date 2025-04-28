from pathlib import Path
import sys

sys.setrecursionlimit(10000)


START = "S"
END = "E"
WALL = "#"
FREE = "."
INF_SCORE = 1_000_000_00
END_LOWEST_SCORE: int = INF_SCORE
ALREADY_ENDED: bool = False


def read_input(file: str) -> list[list[str]]:
    data = Path(file).read_text().splitlines()
    return [list(l) for l in data]

def draw_maze(maze: list[list[str]]) -> str:
    return "\n".join(["".join([f"{x}" for x in row]) for row in maze])

def find_start(maze, match) -> tuple[int, int]:
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == match:
                return i, j
    return -1, -1

class Position:
    def __init__(self, row: int, col: int, drow: int, dcol: int, score: int, next = None):
        self.row = row
        self.col = col
        self.drow = drow
        self.dcol = dcol
        self.score = score
        self.next = next

    def __str__(self):
        return f"POSITION: {(self.row, self.col, self.drow, self.dcol, self.score)}"


if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    file = f"./{filename}.txt"
    maze = read_input(file)

    print(draw_maze(maze))

    ## I NEED TO SAVE THE DIRECTION I ARRIVED
    directions = [
        (1, 0), (-1, 0), (0, 1), (0, -1)
    ]

    end_row, end_col = find_start(maze, END)
    end_score = 0
    end_position = Position(
        row=end_row, col=end_col, drow=0, dcol=0, score=0, next=None
    )
    memo = {(end_row, end_col): end_position}

    possible_position_to_arrive_at_end = []
    for drow, dcol in directions:
        if maze[end_row + drow][end_col + dcol] == FREE:
            position = Position(
                row = end_row + drow,
                col = end_col + dcol,
                drow = -drow,
                dcol = -dcol,
                score = 1 + end_position.score,
                next = end_position
            )
            memo[(position.row, position.col)] = position
            possible_position_to_arrive_at_end.append(position)

    current_positions: list[Position] = possible_position_to_arrive_at_end.copy()

    turns = 0
    while len(current_positions) > 0:
        next_points = []
        for position in current_positions:
            unavailable_position: Position = position.next
            unavailable_row, unavailable_col = unavailable_position.row, unavailable_position.col

            for drow, dcol in directions:
                next_row, next_col = position.row + drow, position.col + dcol
                
                if (next_row, next_col) == (unavailable_row, unavailable_col):
                    continue

                next_symbol = maze[next_row][next_col]
                
                if next_symbol == WALL:
                    continue

                same_direction = (-drow, -dcol) == (position.drow, position.dcol)
                score = 1 + position.score
                if not same_direction:
                    score += 1000

                next_position = Position(
                    row=next_row,
                    col=next_col,
                    drow=-drow,
                    dcol=-dcol,
                    score=score,
                    next=position
                )

                should_continue_path = False
                memo_key = (next_row, next_col)
                if memo_key not in memo:
                    memo[memo_key] = next_position
                    should_continue_path = True
                else:
                    memo_position = memo[memo_key]
                    if next_position.score < memo_position.score:
                        memo[memo_key] = next_position
                        should_continue_path = True

                if should_continue_path:
                    next_points.append(next_position)
            

        current_positions = next_points.copy()
        turns += 1

    srow, scol = find_start(maze, START)
    print(memo[(srow, scol)].score + 1000)
