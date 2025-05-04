from pathlib import Path


def read_input(file: str):
    data = Path(file).read_text().splitlines()
    return [list(l) for l in data]


NUMPAD = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
    "#": (3, 0),
}

MOVEMENTS = {(-1, 0): "^", (1, 0): "v", (0, -1): "<", (0, 1): ">", (0, 0): ""}

DIRPAD = {"^": (0, 1), "A": (0, 2), "<": (1, 0), "v": (1, 1), ">": (1, 2), "#": (0, 0)}


def solve_sequence(current_button: str, next_button: str, pos_dict: dict) -> set:
    inverted_pos_dict = {v: k for k, v in pos_dict.items()}

    start_position = pos_dict[current_button]
    next_position = pos_dict[next_button]

    distance_row = next_position[0] - start_position[0]
    distance_col = next_position[1] - start_position[1]

    row_norm = max(abs(distance_row), 1)
    col_norm = max(abs(distance_col), 1)
    direction_row = distance_row // row_norm
    direction_col = distance_col // col_norm

    directions = ["row", "col"]

    if inverted_pos_dict[(next_position[0], start_position[1])] == "#":
        directions.remove("row")
    if inverted_pos_dict[(start_position[0], next_position[1])] == "#":
        directions.remove("col")

    possible_paths = set()
    for dir in directions:
        if dir == "row":
            possible_paths.add(
                row_norm * MOVEMENTS[(direction_row, 0)]
                + col_norm * MOVEMENTS[(0, direction_col)]
                + "A"
            )
        if dir == "col":
            possible_paths.add(
                col_norm * MOVEMENTS[(0, direction_col)]
                + row_norm * MOVEMENTS[(direction_row, 0)]
                + "A"
            )

    return possible_paths


def solve_robot2(sequence: str):
    current_sequence = "A" + sequence
    result = 0
    for i in range(0, len(current_sequence) - 1):
        current_button = current_sequence[i]
        next_button = current_sequence[i + 1]
        possible_paths = solve_sequence(
            current_button=current_button, next_button=next_button, pos_dict=DIRPAD
        )
        result += min(len(p) for p in possible_paths)
    return result


def solve_robot1(sequence: str) -> int:

    current_sequence = "A" + sequence
    result = 0
    for i in range(0, len(current_sequence) - 1):
        current_button = current_sequence[i]
        next_button = current_sequence[i + 1]
        possible_paths = solve_sequence(
            current_button=current_button, next_button=next_button, pos_dict=DIRPAD
        )

        solutions = []
        for path in possible_paths:
            _solution = solve_robot2(path)
            solutions.append(_solution)

        result += min(solutions)

    return result


if __name__ == "__main__":

    import sys

    _filename = sys.argv[1]
    filename = f"{_filename}.txt"

    sequences = read_input(filename)

    global_result = 0

    for sequence in sequences:
        current_sequence = ["A"] + sequence
        result = 0
        for i in range(0, len(current_sequence) - 1):
            current_button = current_sequence[i]
            next_button = current_sequence[i + 1]
            possible_paths0 = solve_sequence(
                current_button=current_button, next_button=next_button, pos_dict=NUMPAD
            )

            solutions = []
            for path in possible_paths0:
                _solution = solve_robot1(path)
                solutions.append(_solution)

            result += min(solutions)
        global_result += result * int("".join(sequence[:-1]))

    print(global_result)
