from pathlib import Path
from enum import Enum

N = 12

boxes = [
    (0, 3),
    (0, 4),
    (1, 1),
    (1, 11),
    (2, 8),
    (3, 0),
    (3, 11),
    (4, 2),
    (5, 4),
    (5, 7),
    (6, 0),
    (6, 9),
    (7, 3),
    (7, 11),
    (8, 10),
    # (9, 0),
    (10, 5),
    (10, 8),
    # (2, 10),
]

stat_row, start_col = 8, 1


class Markers(Enum):
    START = "^"
    OBJECT = "#"
    CLEARED = "X"
    FREE = "."


file_name = "fer_sample01.txt"

data = []
for i in range(N):
    row = []
    for j in range(N):
        if (i, j) in boxes:
            mark = Markers.OBJECT.value
        else:
            mark = Markers.FREE.value
        row.append(mark)
    data.append(row)

data[stat_row][start_col] = Markers.START.value

text = "\n".join(["".join(row) for row in data])
Path(file_name).write_text(text)
