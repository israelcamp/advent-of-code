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

def find_start(maze) -> tuple[int, int]:
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == START:
                return i, j

def find_next_directions(row: int, col: int, maze, current_direction: tuple[int, int]):
    new_directions = []

    clockwise_dcol, clockwise_drow = rotate_vector(current_direction[1], current_direction[0], 90)
    anticlockwise_dcol, anticlockwise_drow = rotate_vector(current_direction[1], current_direction[0], -90)
    possible_directions = [
        current_direction,
        (clockwise_drow, clockwise_dcol), 
        (anticlockwise_drow, anticlockwise_dcol)
    ]

    for drow, dcol in possible_directions:
        next_row, next_col = row + drow, col + dcol
        if maze[next_row][next_col] != WALL:
            new_directions.append((drow, dcol))

    return new_directions

def find_min_path(row: int, col: int, maze, current_direction: tuple[int, int], visited: list[tuple[int, int]], memo: dict) -> int:
    forward_visited = visited.copy()

    if (row, col, *current_direction) in memo:
        return memo[(row, col, *current_direction)]


    next_row, next_col = row + current_direction[0], col + current_direction[1]
    if maze[next_row][next_col] == END:
        return 0

    next_directions = find_next_directions(next_row, next_col, maze, current_direction)
    if len(next_directions) == 0:
        memo[(row, col, *current_direction)] = 4e10
        return 5e10

    results = []
    for next_dir in next_directions:

        path_score = find_min_path(next_row, next_col, maze, next_dir, forward_visited, memo)

        score = 1
        if next_dir != current_direction:
            score += 1000
        r = score + path_score
        results.append(r)
    
    print(row, col, results)
    result = min(results)

    memo[(row, col, *current_direction)] = result
    
    return result
    

    

if __name__ == "__main__": 
    file = "./sample2.txt"
    maze = read_input(file)

    print(draw_maze(maze))

    start_row, start_col = find_start(maze)
    start_direction = (0, -1)
    row, col = start_row, start_col + 1

    # print(rotate_vector(start_direction[1], start_direction[0], -90))
    # print(rotate_vector(*start_direction, -90))

    # print(rotate_vector(1, 0, 90))
    # print(rotate_vector(1, 0, -90))
    visited = []
    memo = {}
    result = find_min_path(row, col, maze, start_direction, visited, memo)

    print(result)


    


