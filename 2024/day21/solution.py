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
    "#": (3, 0)
}

MOVEMENTS = {
    (-1, 0): "^",
    (1, 0): "v",
    (0, -1): "<",
    (0, 1): ">",
    (0,0): ""
}

DIRPAD = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
    "#": (0,0)
}

def solve_sequence(start_button: str, pos_dict: dict, current_sequence: str) -> str:
    start_position = pos_dict[start_button]
    inverted_pos_dict = {v:k for k,v in pos_dict.items()}

    movement_sequence = ""
    for next_button in current_sequence:
        next_position = pos_dict[next_button]

        distance_row = next_position[0] - start_position[0]
        distance_col = next_position[1] - start_position[1]

        row_norm = max(abs(distance_row), 1)
        col_norm = max(abs(distance_col), 1)
        direction_row = distance_row // row_norm
        direction_col = distance_col // col_norm

        next_row = start_position[0] + distance_row
        if inverted_pos_dict[(next_row, 0)] == "#":
            preference = "col"
        elif inverted_pos_dict[(0, start_position[1] + distance_col)] == "#":
            preference = "row"
        else:
            preference = "col"

        if preference == "row":
            movement_sequence += row_norm * MOVEMENTS[(direction_row, 0)] + col_norm * MOVEMENTS[(0, direction_col)]
        else:
            movement_sequence += col_norm * MOVEMENTS[(0, direction_col)] + row_norm * MOVEMENTS[(direction_row, 0)]
        movement_sequence += "A"
        
        start_button = next_button
        start_position = next_position

    return movement_sequence

if __name__ == "__main__":

    import sys
    _filename = sys.argv[1]
    filename = f"{_filename}.txt"

    sequences = read_input(filename)
    current_sequence = sequences[0]


    results = 0
    for current_sequence in sequences:
        numpad_sequence = solve_sequence(start_button="A", pos_dict=NUMPAD, current_sequence=current_sequence,)
        robot1_sequence = solve_sequence(start_button="A", pos_dict=DIRPAD, current_sequence=numpad_sequence, )
        robot2_sequence = solve_sequence(start_button="A", pos_dict=DIRPAD, current_sequence=robot1_sequence, )
        print(len(robot2_sequence), "".join(current_sequence))
        results += len(robot2_sequence) * int("".join(current_sequence[:-1]))

    print(results)
    # print(robot2_sequence)
    # print(robot1_sequence)
    # print(numpad_sequence)