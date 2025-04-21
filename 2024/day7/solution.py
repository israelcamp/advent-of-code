from pathlib import Path
from typing import List, Tuple

InputType = List[Tuple[int, List[int]]]


def read_input(file: str) -> InputType:
    lines = Path(file).read_text().splitlines()
    data = []
    for line in lines:
        line_numbers = line.split()
        result = line_numbers[0]
        values = line_numbers[1:]
        result = result.replace(":", "")
        data.append((int(result), [int(v) for v in values]))
    return data


class Node:
    def __init__(self, previous, operation: str, value: int, seem: list):
        self.previous = previous
        self.operation = operation
        self.value = value
        self.seem = seem


class FoundValue(Exception):
    pass


class NotFoundValue(Exception):
    pass


def add_nodes(
    node: Node, values: list[int], goal: int, depth: int, max_depth: int
) -> Node:
    if depth == max_depth:
        return node

    assert depth < len(values), f"Depth {depth} exceeds values length {len(values)}"

    next_value = values[depth]
    left_node = Node(
        previous=node,
        operation="+",
        value=node.value + next_value,
        seem=node.seem + [next_value],
    )
    right_node = Node(
        previous=node,
        operation="*",
        value=node.value * next_value,
        seem=node.seem + [next_value],
    )
    middle_node = Node(
        previous=node,
        operation="||",
        value=int(str(node.value) + str(next_value)),
        seem=node.seem + [next_value],
    )

    if depth == max_depth - 1:
        # print("HEYO", depth, max_depth)
        assert left_node.seem == values
        assert right_node.seem == values

        if left_node.value == goal:
            err = FoundValue()
            err.node = left_node
            raise err
        if right_node.value == goal:
            err = FoundValue()
            err.node = right_node
            raise err
        if middle_node.value == goal:
            err = FoundValue()
            err.node = middle_node
            raise err

        # raise NotFoundValue()

    else:
        if left_node.value <= goal:
            add_nodes(
                node=left_node,
                values=values,
                goal=goal,
                depth=depth + 1,
                max_depth=max_depth,
            )
        if right_node.value <= goal:
            add_nodes(
                node=right_node,
                values=values,
                goal=goal,
                depth=depth + 1,
                max_depth=max_depth,
            )
        if middle_node.value <= goal:
            add_nodes(
                node=middle_node,
                values=values,
                goal=goal,
                depth=depth + 1,
                max_depth=max_depth,
            )

    return node


if __name__ == "__main__":
    file = "./input2.txt"
    data = read_input(file)

    nodes = []
    result = 0
    not_possible = []
    for i, line in enumerate(data):
        (test_result, values) = line
        # if i != 10:
        #     continue
        # print(test_result, values)

        start_node = Node(
            previous=None, operation=None, value=values[0], seem=[values[0]]
        )

        try:
            add_nodes(start_node, values, test_result, depth=1, max_depth=len(values))
        except FoundValue as e:
            nodes.append(e.node)
            result += test_result
        else:
            not_possible.append((test_result, values))

    # node = nodes[-1]
    # operations = [node.operation]
    # previous = node.previous
    # while previous.previous is not None:
    #     operations = [previous.operation] + operations
    #     previous = previous.previous

    # current_expression_list = [str(values[0])]
    # for v, op in zip(values[1:], operations):
    #     current_expression_list += [op, str(v)]
    # expression = "".join(current_expression_list)
    # print(test_result, "=", expression, "=", eval(expression))

    # assert len(data) == len(nodes) + len(not_possible)

    print("RESULT", result)
    # print(not_possible)
