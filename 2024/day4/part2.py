from pathlib import Path


def read_input(file: str) -> list[list[str]]:
    data = Path(file).read_text()
    lines = data.splitlines()
    return [list(l.replace(" ", "")) for l in lines]


def forward_word(row: list[str], j: int, query: str) -> bool:
    m = len(row)
    query_size = len(query)
    if j + query_size > m:
        return False

    word = "".join(row[j : j + query_size])
    return word == query


def backwards_word(row: list[str], j: int, query: str):
    return forward_word(list(reversed(row)), len(row) - j - 1, query)


def build_column(data: list[list[str]], colj: int) -> list[str]:
    return [row[colj] for row in data]


def build_right_diagonal(
    data: list[list[str]], rowi: int, colj: int
) -> tuple[list[str], int]:
    initial_rowi, initial_colj = rowi, colj

    down = [data[rowi][colj]]
    N, M = len(data), len(data[0])
    while True:
        rowi = rowi + 1
        colj = colj + 1

        if rowi >= N or colj >= M:
            break

        down.append(data[rowi][colj])

    rowi, colj = initial_rowi, initial_colj
    up = []
    while True:
        rowi = rowi - 1
        colj = colj - 1

        if rowi < 0 or colj < 0:
            break

        up.append(data[rowi][colj])

    diagonal = list(reversed(up)) + down
    new_j = len(up)
    return diagonal, new_j


def build_left_diagonal(
    data: list[list[str]], rowi: int, colj: int
) -> tuple[list[str], int]:
    initial_rowi, initial_colj = rowi, colj

    down = [data[rowi][colj]]
    N, M = len(data), len(data[0])
    while True:
        rowi = rowi + 1
        colj = colj - 1

        if rowi >= N or colj < 0:
            break

        down.append(data[rowi][colj])

    rowi, colj = initial_rowi, initial_colj
    up = []
    while True:
        rowi = rowi - 1
        colj = colj + 1

        if rowi < 0 or colj >= M:
            break

        up.append(data[rowi][colj])

    diagonal = list(reversed(up)) + down
    new_j = len(up)
    return diagonal, new_j


if __name__ == "__main__":

    data = read_input("./input.txt")
