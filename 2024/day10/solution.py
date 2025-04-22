from pathlib import Path


def read_input(file: str) -> list[list[int]]:
    data = Path(file).read_text()
    lines = data.splitlines()
    return [[int(l) for l in line] for line in lines]


class Node:

    def __init__(
        self, root, parent, height: int, end_count: int = 0, trailheads: set = set()
    ):
        self.root = root
        self.parent = parent
        self.height = height
        self.end_count = end_count
        self.trailheads = trailheads


def walk(data: list[list[int]], row: int, col: int, root: Node, parent: Node) -> Node:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for i, j in directions:
        next_row, next_col = row + i, col + j
        if (
            next_row < 0
            or next_row >= len(data)
            or next_col < 0
            or next_col >= len(data[0])
        ):
            continue

        next_height = data[next_row][next_col]
        if parent.height + 1 != next_height:
            continue

        if next_height == 9:
            root.end_count += 1
            root.trailheads.add((next_row, next_col))
        else:
            node = Node(root=root, parent=parent, height=next_height, trailheads=set())
            walk(data=data, row=next_row, col=next_col, root=root, parent=node)

    return root


if __name__ == "__main__":
    file = "./sample.txt"
    data = read_input(file)

    N, M = len(data), len(data[0])

    starting_points = []
    for i in range(N):
        for j in range(M):
            if data[i][j] == 0:
                starting_points.append((i, j))

    result = 0
    result_part_two = 0
    for starting_row, starting_col in starting_points:
        root = Node(root=None, parent=None, height=0, end_count=0, trailheads=set())

        root = walk(data, starting_row, starting_col, root=root, parent=root)
        result += len(root.trailheads)
        result_part_two += root.end_count

    print("RESUL PART ONE", result)
    print("RESUL PART TWO", result_part_two)
