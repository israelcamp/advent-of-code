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

    influence_vars.add(target)
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


def is_valid(wanted_index: int, operations: list):
    target_z = get_wire_string("z", wanted_index)
    previous_z = get_wire_string("z", wanted_index - 1)
    previous_previous_z = get_wire_string("z", wanted_index - 2)

    prev_influenced_vars = find_influence_wires(previous_z)
    prev_prev_influenced_vars = find_influence_wires(previous_previous_z)
    previous_influence_operations = find_operations_from_vars(
        prev_influenced_vars - prev_prev_influenced_vars, operations
    )

    previous_x = get_wire_string("x", wanted_index - 1)
    previous_y = get_wire_string("y", wanted_index - 1)
    previous_c1 = None
    previous_a1 = None
    for top in previous_influence_operations:
        if top[1] == "OR":
            previous_c1 = top[-1]
        if set(top[:-1]) == {previous_x, previous_y, "XOR"}:
            previous_a1 = top[-1]

    target_x = get_wire_string("x", wanted_index)
    target_y = get_wire_string("y", wanted_index)

    # lets find the value for a1
    a1_vars = {target_x, target_y, "XOR"}
    a1_op = get_op_from_vars(a1_vars, operations)
    a1 = a1_op[-1] if a1_op is not None else None

    # lets find a2
    a2_vars = {previous_x, previous_y, "AND"}
    a2_op = get_op_from_vars(a2_vars, operations)
    a2 = a2_op[-1] if a2_op is not None else None

    # lets find b1
    b1_vars = {previous_c1, previous_a1, "AND"}
    b1_op = get_op_from_vars(b1_vars, operations)
    b1 = b1_op[-1] if b1_op is not None else None

    # lets find c1
    c1_vars = {b1, "OR", a2}
    c1_op = get_op_from_vars(c1_vars, operations)
    c1 = c1_op[-1] if c1_op is not None else None

    # so now lets find the c1 XOR a1 that should produce z
    z_vars = {c1, "XOR", a1}
    z_op = get_op_from_vars(z_vars, operations)
    z = z_op[-1] if z_op is not None else None

    return z == target_z, a1, c1, previous_a1, previous_c1


def get_op_from_vars(vars: set, operations: list):
    for op in operations:
        if set(op[:-1]) == vars:
            return op
    return None


def get_op_from_out(out: str, operations: list):
    for op in operations:
        if op[-1] == out:
            return op
    return None


def fix_wire(wanted_index: int, operations: list):
    target_z = get_wire_string("z", wanted_index)
    previous_z = get_wire_string("z", wanted_index - 1)
    previous_previous_z = get_wire_string("z", wanted_index - 2)

    prev_influenced_vars = find_influence_wires(previous_z)
    prev_prev_influenced_vars = find_influence_wires(previous_previous_z)
    previous_influence_operations = find_operations_from_vars(
        prev_influenced_vars - prev_prev_influenced_vars, operations
    )

    previous_x = get_wire_string("x", wanted_index - 1)
    previous_y = get_wire_string("y", wanted_index - 1)
    previous_c1 = None
    previous_a1 = None
    for top in previous_influence_operations:
        if top[1] == "OR":
            previous_c1 = top[-1]
        if set(top[:-1]) == {previous_x, previous_y, "XOR"}:
            previous_a1 = top[-1]

    target_x = get_wire_string("x", wanted_index)
    target_y = get_wire_string("y", wanted_index)

    # lets find the value for a1
    a1_vars = {target_x, target_y, "XOR"}
    a1_op = get_op_from_vars(a1_vars, operations)
    a1 = a1_op[-1] if a1_op is not None else None

    # lets find a2
    a2_vars = {previous_x, previous_y, "AND"}
    a2_op = get_op_from_vars(a2_vars, operations)
    a2 = a2_op[-1] if a2_op is not None else None

    # lets find b1
    b1_vars = {previous_c1, previous_a1, "AND"}
    b1_op = get_op_from_vars(b1_vars, operations)
    b1 = b1_op[-1] if b1_op is not None else None

    # lets find c1
    c1_vars = {b1, "OR", a2}
    c1_op = get_op_from_vars(c1_vars, operations)
    c1 = c1_op[-1] if c1_op is not None else None

    # so now lets find the c1 XOR a1 that should produce z
    z_vars = {c1, "XOR", a1}
    z_op = get_op_from_vars(z_vars, operations)
    z = z_op[-1] if z_op is not None else None

    assert all(v is not None for v in (a1, a2, b1, c1))
    if z is None:
        target_z_op = get_op_from_out(target_z, operations)
        target_z_vars = {target_z_op[0], target_z_op[2]}

        if c1 not in target_z_vars and a1 in target_z_vars:
            need_to_swap = {c1}.union(target_z_vars - {a1})
        elif a1 not in target_z_vars and c1 in target_z_vars:
            need_to_swap = {a1}.union(target_z_vars - {c1})
        else:
            raise Exception("NONE PRESENT")
        to_swap = list(need_to_swap)
        swap_outs(to_swap[0], to_swap[1], operations)
        return to_swap

    if z != target_z:
        swap_outs(z, target_z, operations)
        return [z, target_z]


def swap_outs(var1: str, var2: str, operations: list):
    var1_op = get_op_from_out(var1, operations)
    var2_op = get_op_from_out(var2, operations)

    new_op1 = var1_op[:-1] + (var2,)
    new_op2 = var2_op[:-1] + (var1,)

    operations.remove(var1_op)
    operations.remove(var2_op)

    operations.append(new_op1)
    operations.append(new_op2)


if __name__ == "__main__":
    import sys

    filename = f"{sys.argv[1]}.txt"
    known_values, operations = read_input(filename)

    N = 45
    swapped_vars = []
    for idx in range(4, N):
        valid, *vars = is_valid(idx, operations)
        if not valid:
            swapped = fix_wire(idx, operations)
            swapped_vars += swapped

    print(",".join(sorted(swapped_vars)))
