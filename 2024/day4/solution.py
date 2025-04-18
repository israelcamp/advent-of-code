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


def solution_part_one():
    data = read_input("./input.txt")

    # print(data[:1])

    N, M = len(data), len(data[0])
    SEARCHED_WORD = "XMAS"

    count = 0
    for i in range(N):
        row = data[i]
        for j in range(M):
            element = row[j]

            if element != SEARCHED_WORD[0]:
                continue

            count += forward_word(row.copy(), j, SEARCHED_WORD)
            count += backwards_word(row.copy(), j, SEARCHED_WORD)

            column = build_column(data.copy(), j)
            count += forward_word(column.copy(), i, SEARCHED_WORD)
            count += backwards_word(column.copy(), i, SEARCHED_WORD)

            diagonal_right, nj = build_right_diagonal(data, i, j)
            count += forward_word(diagonal_right, nj, SEARCHED_WORD)
            count += backwards_word(diagonal_right, nj, SEARCHED_WORD)

            diagonal_left, nj = build_left_diagonal(data, i, j)
            count += forward_word(diagonal_left, nj, SEARCHED_WORD)
            count += backwards_word(diagonal_left, nj, SEARCHED_WORD)

    return count


if __name__ == "__main__":

    data = read_input("./sample.txt")

    # print(data[:1])

    N, M = len(data), len(data[0])
    SEARCHED_WORD = "MAS"

    x_mas_indices_right: list = []
    x_mas_indices_left: list = []
    count = 0
    for i in range(N):
        row = data[i]
        for j in range(M):
            element = row[j]

            if element != SEARCHED_WORD[0]:
                continue

            diagonal_right, nj = build_right_diagonal(data, i, j)
            if forward_word(diagonal_right, nj, SEARCHED_WORD):
                x_mas_indices_right.append(
                    {"M": (i, j), "A": (i + 1, j + 1), "S": (i + 2, j + 2)}
                )

            if backwards_word(diagonal_right, nj, SEARCHED_WORD):
                x_mas_indices_right.append(
                    {"M": (i, j), "A": (i - 1, j - 1), "S": (i - 2, j - 2)}
                )

            diagonal_left, nj = build_left_diagonal(data, i, j)
            if forward_word(diagonal_left, nj, SEARCHED_WORD):
                x_mas_indices_left.append(
                    {"M": (i, j), "A": (i + 1, j - 1), "S": (i + 2, j - 2)}
                )

            if backwards_word(diagonal_left, nj, SEARCHED_WORD):
                x_mas_indices_left.append(
                    {"M": (i, j), "A": (i - 1, j + 1), "S": (i - 2, j + 2)}
                )

    a_right_indices = [x["A"] for x in x_mas_indices_right]
    a_left_indices = [x["A"] for x in x_mas_indices_left]

    print(len(set(a_left_indices).intersection(set(a_right_indices))))
