from pathlib import Path
from typing import List, Tuple
from enum import Enum
from collections import Counter, defaultdict

InputType = List[List[str]]
IndexType = Tuple[int, int]


def read_input(file: str) -> InputType:
    data = Path(file).read_text()
    return [list(l) for l in data.splitlines()]


file = "./fer_sample01.txt"
data = read_input(file)

for row in data:
    print("- " * len(row))
    print("|".join([x if x != "." else x for x in row]))

for i in range(len(data)):
    for j in range(len(data[0])):
        if data[i][j] == "^":
            print(i, j)
