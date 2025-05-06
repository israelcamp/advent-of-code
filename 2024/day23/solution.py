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

    result_one = solution_part_one(connections)
    print("PART ONE")

    all_names = list(connections.keys())
    biggest_set = None
    biggest_len = 0

    name = "ka"
    name_conns = list(connections["ka"])
    for name, name_conns in connections.items():
        for n_name in name_conns:
            this_set = [name, n_name]
            for no_name in name_conns:
                if no_name == n_name:  ## skip the current oin analysis
                    continue
                no_name_conns = connections[no_name]
                if all(x in no_name_conns for x in this_set):
                    this_set.append(no_name)
            if len(this_set) > biggest_len:
                biggest_len, biggest_set = len(this_set), this_set

    print("PART TWO", ",".join(sorted(biggest_set)))
