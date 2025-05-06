from pathlib import Path
from collections import defaultdict


def read_input(file: str) -> list[set]:
    data = Path(file).read_text().splitlines()
    return [set(x.split("-")) for x in data]


def solution_part_one(connections: dict) -> int:
    threeset_connections = []
    for current, current_connections in connections.items():
        for second in current_connections:
            connected_to_second = connections[second]
            for third in current_connections:
                if third == second:
                    continue
                if third not in connected_to_second:
                    continue

                tc = set((current, second, third))
                if tc in threeset_connections:
                    continue
                threeset_connections.append(tc)

    starts_with_t = 0
    for tc in threeset_connections:
        starts_with_t += any(name.startswith("t") for name in tc)
    return starts_with_t


if __name__ == "__main__":
    import sys

    filename = f"{sys.argv[1]}.txt"

    twoset_connections = read_input(filename)

    connections = defaultdict(set)
    for connection_set in twoset_connections:
        for current in connection_set:
            for other in connection_set:
                if current == other:
                    continue
                connections[current].add(other)

    # result_one = solution_part_one(connections)

    all_names = list(connections.keys())
    biggest_set = None
    biggest_len = 0

    current_set_connections = twoset_connections
    while True:
        next_set_connections = []
        for name, name_connections in connections.items():
            for con_set in current_set_connections:
                if not all(x in name_connections for x in con_set):
                    continue
                this_set = con_set.union({name})
                if this_set in next_set_connections:
                    continue
                next_set_connections.append(this_set)

        if len(next_set_connections) > 0:
            current_set_connections = next_set_connections
            continue
        else:
            break

    print(current_set_connections)

    # starts_with_t = 0
    # for tc in next_set_connections:
    #     starts_with_t += any(name.startswith("t") for name in tc)
    # print(starts_with_t)

    # print(biggest_len, biggest_set)``
