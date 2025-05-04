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
    (0, 0): ""
}

DIRPAD = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
    "#": (0, 0)
}

def solve_sequence(current_button: str, next_button:str, pos_dict: dict) -> str:
    inverted_pos_dict = {v:k for k,v in pos_dict.items()}
    
    start_position = pos_dict[current_button]
    next_position = pos_dict[next_button]

    distance_row = next_position[0] - start_position[0]
    distance_col = next_position[1] - start_position[1]

    row_norm = max(abs(distance_row), 1)
    col_norm = max(abs(distance_col), 1)
    direction_row = distance_row // row_norm
    direction_col = distance_col // col_norm

    directions = ["row", "col"]
    if inverted_pos_dict[(next_position[0], 0)] == "#":
        directions.remove("row")
    elif inverted_pos_dict[(0, next_position[1])] == "#":
        directions.remove("col")

    possible_paths = set()
    for dir in directions:
        if dir == "row":
            possible_paths.add(row_norm * MOVEMENTS[(direction_row, 0)] + col_norm * MOVEMENTS[(0, direction_col)] + "A")
        if dir == "col":
            possible_paths.add(col_norm * MOVEMENTS[(0, direction_col)] + row_norm * MOVEMENTS[(direction_row, 0)] + "A")

    return possible_paths

if __name__ == "__main__":

    import sys
    _filename = sys.argv[1]
    filename = f"{_filename}.txt"

    sequences = read_input(filename)
    
    current_sequence = sequences[-1]

    possible_paths_numpad = []
    current_sequence = ["A"] + sequences[-1]
    for i in range(0, len(current_sequence) - 1):
        current_button = current_sequence[i]
        next_button = current_sequence[i+1]
        possible_paths0 = solve_sequence(current_button=current_button, next_button=next_button, pos_dict=NUMPAD)
        possible_paths_numpad.append(possible_paths0)

    print(possible_paths_numpad) # List[set]

    current_paths = possible_paths_numpad[1]
    possible_paths_robot1 = []
    for current_paths in possible_paths_numpad:
        path_solutions = []
        for sequence in current_paths:
            
            current_sequence = ["A"] + list(sequence)
            # print(current_sequence)
            possible_paths = []
            for i in range(0, len(current_sequence) - 1):
                current_button = current_sequence[i]
                next_button = current_sequence[i+1]
                possible_paths1 = solve_sequence(current_button=current_button, next_button=next_button, pos_dict=DIRPAD)
                possible_paths.append(possible_paths1)
            path_solutions.append(possible_paths)
        possible_paths_robot1.append(path_solutions)
    

    print(possible_paths_robot1) # List[List[set]]

   
    current_list = possible_paths_robot1[0]
    solution = 0
    for possible_path_list in current_list:
        print(possible_path_list)

        ## now i choose the set that generate the minimum steps
        for path_sets in possible_path_list:
            print(path_sets)




            break
        break