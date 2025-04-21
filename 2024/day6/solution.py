from pathlib import Path
from typing import List, Tuple
from enum import Enum
from collections import Counter

InputType = List[List[str]]
IndexType = Tuple[int, int]


class Directions(Enum):
    UP = "U"
    DOWN = "D"
    RIGHT = "R"
    LEFT = "L"


class Markers(Enum):
    START = "^"
    OBJECT = "#"
    CLEARED = "X"
    FREE = "."


def read_input(file: str) -> InputType:
    data = Path(file).read_text()
    return [list(l) for l in data.splitlines()]


def starting_index(data: InputType) -> tuple[int, int]:
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == Markers.START.value:
                return i, j
    return -1, -1


class Mover:

    @staticmethod
    def up_index_update(rowi: int, colj: int) -> IndexType:
        return rowi - 1, colj

    @staticmethod
    def up_end_condition(rowi: int, colj: int, num_rows: int, num_cols: int) -> bool:
        return rowi < 0

    @staticmethod
    def right_index_update(rowi: int, colj: int) -> IndexType:
        return rowi, colj + 1

    @staticmethod
    def right_end_condition(rowi: int, colj: int, num_rows: int, num_cols: int) -> bool:
        return colj >= num_cols

    @staticmethod
    def down_index_update(rowi: int, colj: int) -> IndexType:
        return rowi + 1, colj

    @staticmethod
    def down_end_condition(rowi: int, colj: int, num_rows: int, num_cols: int) -> bool:
        return rowi >= num_rows

    @staticmethod
    def left_index_update(rowi: int, colj: int) -> IndexType:
        return rowi, colj - 1

    @staticmethod
    def left_end_condition(rowi: int, colj: int, num_rows: int, num_cols: int) -> bool:
        return colj < 0


DIRECTION_FUNCTIONS = {
    Directions.UP: {
        "update": Mover.up_index_update,
        "condition": Mover.up_end_condition,
        "next": Directions.RIGHT,
    },
    Directions.RIGHT: {
        "update": Mover.right_index_update,
        "condition": Mover.right_end_condition,
        "next": Directions.DOWN,
    },
    Directions.DOWN: {
        "update": Mover.down_index_update,
        "condition": Mover.down_end_condition,
        "next": Directions.LEFT,
    },
    Directions.LEFT: {
        "update": Mover.left_index_update,
        "condition": Mover.left_end_condition,
        "next": Directions.UP,
    },
}


def move_until_object(
    data: InputType, rowi: int, colj: int, direction: Directions, visited: list
):
    direction_funcs = DIRECTION_FUNCTIONS[direction]
    while True:

        next_row, next_col = direction_funcs["update"](rowi, colj)

        if direction_funcs["condition"](next_row, next_col, len(data), len(data[0])):
            visited.append((rowi, colj, direction))
            return data

        if data[next_row][next_col] == Markers.OBJECT.value:
            return move_until_object(data, rowi, colj, direction_funcs["next"], visited)

        visited.append((rowi, colj, direction))

        data[next_row][next_col] = Markers.CLEARED.value
        rowi, colj = next_row, next_col


def solution_part_one(data: InputType) -> tuple[int, list]:
    starting_row, starting_col = starting_index(data)
    data[starting_row][starting_col] = Markers.CLEARED.value
    visited_places: list[Tuple[int, int, Directions]] = []
    data = move_until_object(
        data, starting_row, starting_col, Directions.UP, visited_places
    )
    flatten_data = sum(data, [])
    result = Counter(flatten_data).get(Markers.CLEARED.value, 0)
    return result, visited_places


if __name__ == "__main__":
    file = "./input.txt"
    data_part_one = read_input(file)
    data = read_input(file)

    res_part_one, visited_places = solution_part_one(data_part_one)

    print("PART ONE", res_part_one)

    num_rows, num_cols = len(data), len(data[0])
    print("SHAPE", num_rows, num_cols)
    starting_row, starting_col = starting_index(data)

    boxes_indices = []
    for i in range(num_rows):
        for j in range(num_cols):
            if data[i][j] == Markers.OBJECT.value:
                boxes_indices.append((i, j))

    ###

    ## SAMPLE SOLUTIONS
    ## (6, 3)
    ## (7, 6)
    ## (7, 7)
    ## (8, 1)
    ## (8, 3)
    ## (9, 7)

    loops = []
    already_checked = []
    visited_indices = [(x[0], x[1]) for x in visited_places]
    for current_row, current_col, current_direction in visited_places:
        direction_functions = DIRECTION_FUNCTIONS[current_direction]
        box_row, box_col = direction_functions["update"](current_row, current_col)

        if direction_functions["condition"](box_row, box_col, num_rows, num_cols):
            continue

        if (current_row, current_col) in boxes_indices:
            continue

        if (box_row, box_col) in boxes_indices:
            continue

        if (box_row, box_col) in visited_indices and (
            box_row,
            box_col,
        ) in already_checked:
            continue
        elif (box_row, box_col) in visited_indices:
            already_checked.append((box_row, box_col))

        new_data = read_input(file)
        new_data[box_row][box_col] = Markers.OBJECT.value
        visited = []
        try:
            move_until_object(
                new_data, current_row, current_col, current_direction, visited
            )
        except RecursionError:
            loops.append((box_row, box_col))

    loops = list(set(loops))
    loops = sorted(loops, key=lambda x: x[0])
    loops = list(filter(lambda x: x != (starting_row, starting_col), loops))
    print(len(loops))
