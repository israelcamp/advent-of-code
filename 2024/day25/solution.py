from pathlib import Path
from itertools import product


def read_input(file: str):
    matrices = Path(file).read_text().split("\n\n")

    schematics = []
    keys = []

    for m in matrices:
        if m.startswith("#"):
            schematics.append(m)
        else:
            keys.append(m)
    return schematics, keys


def calculate_keys_height(raw_matrix: str):
    lines = raw_matrix.splitlines()
    matrix = [list(l) for l in lines]
    columns = len(matrix[0])
    N = len(matrix)
    heights = []

    for col in range(columns):
        h = sum(matrix[i][col] == "#" for i in range(N)) - 1
        heights.append(h)
    return heights


if __name__ == "__main__":
    import sys

    filename = f"{sys.argv[1]}.txt"
    H = 7
    W = 5

    raw_schemas, raw_keys = read_input(filename)

    keys_height = []
    for mkey in raw_keys:
        heights = calculate_keys_height(mkey)
        keys_height.append(heights)

    schemas_height = []
    for mschem in raw_schemas:
        heights = calculate_keys_height(mschem)
        schemas_height.append(heights)

    MAX_SUM = H - 2
    fit = 0
    for schema, key in product(schemas_height, keys_height):
        hs = (s + k for s, k in zip(schema, key))
        fit += all(v <= MAX_SUM for v in hs)
    print(fit)
