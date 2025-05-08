from pathlib import Path
from itertools import product, permutations


def read_input(file: str):
    start, operations = Path(file).read_text().split("\n\n")

    known_values = {}
    for line in start.splitlines():
        name, value = line.split()
        name = name.replace(":", "")
        value = int(value)
        known_values[name] = value

    ops = []
    for line in operations.splitlines():
        var1, op, var2, _, out = line.split()
        ops.append((var1, op, var2, out))

    return known_values, ops


OP_TO_FUNC = {
    "XOR": lambda x: 1 * (x[0] ^ x[1]),
    "OR": lambda x: 1 * (x[0] or x[1]),
    "AND": lambda x: 1 * (x[0] and x[1]),
}


def solve_for_xyz(known_values, k="z"):
    result = 0
    for key, value in known_values.items():
        if not key.startswith(k):
            continue
        power = int(key[1:])
        result += value * (2**power)
    return result


def solution_part_one(known_values, operations):
    update_known_values(known_values, operations)
    result = solve_for_xyz(known_values)
    return result


def update_known_values(known_values, operations):
    while True:
        done_ops = 0
        for op in operations:
            var1, op, var2, out = op

            if (
                var1 not in known_values
                or var2 not in known_values
                or out in known_values
            ):
                continue

            known_values[out] = OP_TO_FUNC[op]((known_values[var1], known_values[var2]))
            done_ops += 1
        if done_ops == 0:
            break
    return


def calculate_from_string(vstring: str) -> int:
    return sum([int(v) * (2**i) for i, v in enumerate(reversed(vstring))])

def find_influence_wires(target: str) -> set:
    influence_vars = set()
    idx = 0
    current_op = operations[idx]
    while current_op[-1] != target:
        idx += 1
        current_op = operations[idx]

    influence_vars = {current_op[0], current_op[2]}
    current_vars = influence_vars
    while len(current_vars) > 0:
        next_vars = set()
        for this_operation in operations:
            if this_operation[-1] in current_vars:
                next_vars.add(this_operation[0])
                next_vars.add(this_operation[2])
        influence_vars = influence_vars.union(next_vars)
        current_vars = next_vars

    return influence_vars


def find_operations_from_vars(vars_set: set, operations):
    ops = []
    for op in operations:
        if op[-1] in vars_set:
            # ops.append(f"{op[0]} {op[1]} {op[2]} => {op[-1]}")
            ops.append(op)
    return ops


def get_wire_string(n: str, v: int):
    return f"{n}{str(v).zfill(2)}"

def print_operations(ops: list) -> str:
    for op in ops:
        print(f"{op[0]} {op[1]} {op[2]} => {op[-1]}")

if __name__ == "__main__":
    import sys

    filename = f"{sys.argv[1]}.txt"
    known_values, operations = read_input(filename)

    N = 45
    z_sets = {}
    for i in range(N + 1):
        target = f"z{str(i).zfill(2)}"
        influence_vars = find_influence_wires(target)
        influence_vars.add(target)

        z_sets[target] = influence_vars


    wanted_index = 10
    target_z = f"z{str(wanted_index).zfill(2)}"
    previous_z = f"z{str(wanted_index-1).zfill(2)}"
    previous_previous_z = f"z{str(wanted_index-2).zfill(2)}"

    target_influence_operations = find_operations_from_vars(
        z_sets[target_z] - z_sets[previous_z], operations
    )
    print_operations(target_influence_operations)