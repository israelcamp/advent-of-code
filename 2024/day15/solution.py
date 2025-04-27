from pathlib import Path

UP = "^"
DOWN = "v"
RIGHT = ">"
LEFT = "<"

BOX = "O"
WALL = "#"
ROBOT = "@"
FREE = "."
WBOX_LEFT = "["
WBOX_RIGHT = "]"


def read_input(file: str):
    data = Path(file).read_text()

    grid, commands = data.split("\n\n")

    board = [list(line) for line in grid.splitlines()]
    commands = commands.replace("\n", "").strip()

    return board, commands


def draw_grid(grid: str) -> str:
    return "\n".join(["".join(row) for row in grid])


def find_start(grid) -> tuple[int, int]:
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == ROBOT:
                return i, j
    return -1, -1


def move(grid, row: int, col: int, direction: str):
    if direction == UP:
        drow, dcol = -1, 0
    elif direction == DOWN:
        drow, dcol = 1, 0
    elif direction == RIGHT:
        drow, dcol = 0, 1
    elif direction == LEFT:
        drow, dcol = 0, -1

    next_row, next_col = row + drow, col + dcol
    if grid[next_row][next_col] == WALL:
        return row, col

    if grid[next_row][next_col] == FREE:
        grid[row][col] = FREE
        grid[next_row][next_col] = ROBOT
        return next_row, next_col

    boxes_indices = [(next_row, next_col)]
    distance = 1
    while grid[next_row + drow * distance][next_col + dcol * distance] == BOX:
        boxes_indices.append((next_row + drow * distance, next_col + dcol * distance))
        distance += 1

    # nothing moves
    if grid[next_row + drow * distance][next_col + dcol * distance] == WALL:
        return row, col

    grid[row][col] = FREE
    grid[next_row][next_col] = ROBOT
    for box_row, box_col in boxes_indices:
        grid[box_row + drow][box_col + dcol] = BOX

    return next_row, next_col


def calculate(grid) -> int:
    result = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == BOX or grid[i][j] == WBOX_LEFT:
                result += 100 * i + j
    return result


def transform_grid(grid):
    new_grid = []
    for row in grid:
        new_row = []
        for obj in row:
            if obj == BOX:
                new_row.extend([WBOX_LEFT, WBOX_RIGHT])
            elif obj == WALL:
                new_row.extend([WALL] * 2)
            elif obj == FREE:
                new_row.extend([FREE] * 2)
            elif obj == ROBOT:
                new_row.extend([ROBOT, FREE])
        new_grid.append(new_row)
    return new_grid


def move_wide(grid, row: int, col: int, direction: str):
    if direction == UP:
        drow, dcol = -1, 0
    elif direction == DOWN:
        drow, dcol = 1, 0
    elif direction == RIGHT:
        drow, dcol = 0, 1
    elif direction == LEFT:
        drow, dcol = 0, -1

    next_row, next_col = row + drow, col + dcol
    if grid[next_row][next_col] == WALL:
        return row, col

    if grid[next_row][next_col] == FREE:
        grid[row][col] = FREE
        grid[next_row][next_col] = ROBOT
        return next_row, next_col

    if grid[next_row][next_col] in (WBOX_LEFT, WBOX_RIGHT) and direction in (
        LEFT,
        RIGHT,
    ):
        nn_row, nn_col = next_row, next_col
        boxes_indices = [(nn_row, nn_col, grid[nn_row][nn_col])]

        distance = 1
        nn_row = next_row + drow * distance
        nn_col = next_col + dcol * distance
        while grid[nn_row][nn_col] in (WBOX_LEFT, WBOX_RIGHT):
            boxes_indices.append((nn_row, nn_col, grid[nn_row][nn_col]))
            distance += 1
            nn_row = next_row + drow * distance
            nn_col = next_col + dcol * distance

        # nothing moves
        if grid[nn_row][nn_col] == WALL:
            return row, col

        grid[row][col] = FREE
        grid[next_row][next_col] = ROBOT
        for box_row, box_col, obj in boxes_indices:
            grid[box_row + drow][box_col + dcol] = obj

        return next_row, next_col

    if grid[next_row][next_col] == WBOX_LEFT:
        box_touched = [
            (next_row, next_col, WBOX_LEFT),
            (next_row, next_col + 1, WBOX_RIGHT),
        ]
    elif grid[next_row][next_col] == WBOX_RIGHT:
        box_touched = [
            (next_row, next_col - 1, WBOX_LEFT),
            (next_row, next_col, WBOX_RIGHT),
        ]

    boxes_touched = box_touched
    current_boxes_touched = boxes_touched.copy()
    while True:

        next_boxes_touched = []
        for brow, bcol, bside in current_boxes_touched:
            next_brow, next_bcol = brow + drow, bcol + dcol

            if (next_brow, next_bcol, bside) in next_boxes_touched:
                continue

            next_obj = grid[next_brow][next_bcol]

            if next_obj == WALL:
                return row, col  # does not move

            if next_obj == WBOX_LEFT:
                next_boxes_touched.extend(
                    [
                        (next_brow, next_bcol, WBOX_LEFT),
                        (next_brow, next_bcol + 1, WBOX_RIGHT),
                    ]
                )
            elif next_obj == WBOX_RIGHT:
                next_boxes_touched.extend(
                    [
                        (next_brow, next_bcol - 1, WBOX_LEFT),
                        (next_brow, next_bcol, WBOX_RIGHT),
                    ]
                )
        if len(next_boxes_touched) == 0:
            break

        current_boxes_touched = next_boxes_touched.copy()
        boxes_touched.extend(next_boxes_touched)

    for brow, bcol, bside in reversed(boxes_touched):
        grid[brow + drow][bcol + dcol] = bside
        grid[brow][bcol] = FREE

    grid[next_row][next_col] = ROBOT
    grid[row][col] = FREE

    return next_row, next_col


if __name__ == "__main__":
    file = "./input.txt"
    grid, movements = read_input(file)

    start_row, start_col = find_start(grid)

    row, col = start_row, start_col
    for mv in movements:
        row, col = move(grid, row, col, mv)

    print("RESULT PART ONE", calculate(grid))

    widen_grid = transform_grid(grid)
    print(draw_grid(widen_grid))

    start_row, start_col = find_start(widen_grid)
    row, col = start_row, start_col
    for mv in movements:
        row, col = move_wide(widen_grid, row, col, mv)

    print(draw_grid(widen_grid))
    print("RESULT PART TWO", calculate(widen_grid))
