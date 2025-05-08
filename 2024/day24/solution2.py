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


def get_derangements(elements):
    """
    Generates a list of derangements for a given list of elements.

    Args:
      elements: A list of unique elements.

    Returns:
      A list of lists, where each inner list is a derangement of the input elements.
    """
    n = len(elements)
    derangements = []
    for perm in permutations(elements):
        is_derangement = True
        for i in range(n):
            if perm[i] == elements[i]:
                is_derangement = False
                break
        if is_derangement:
            derangements.append(list(perm))
    return derangements


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


def complete_vars_for_z(wanted_index: int, z_sets: dict, operations: list):
    target = f"z{str(wanted_index).zfill(2)}"
    previous = f"z{str(wanted_index-1).zfill(2)}"
    previous_previous = f"z{str(wanted_index-2).zfill(2)}"

    target_influence_operations = find_operations_from_vars(
        z_sets[target] - z_sets[previous], operations
    )
    previous_influence_operations = find_operations_from_vars(
        z_sets[previous] - z_sets[previous_previous], operations
    )

    previous_x = get_wire_string("x", wanted_index - 1)
    previous_y = get_wire_string("y", wanted_index - 1)
    previous_or_output_var = None
    previous_xy_xor_output_var = None
    for top in previous_influence_operations:
        if top[1] == "OR":
            previous_or_output_var = top[-1]
        if set(top[:-1]) == {previous_x, previous_y, "XOR"}:
            previous_xy_xor_output_var = top[-1]

    target_x = get_wire_string("x", wanted_index)
    target_y = get_wire_string("y", wanted_index)
    a1_vars = {previous_x, previous_y, "AND"}
    a2_vars = {target_x, target_y, "XOR"}
    b1_vars = {previous_or_output_var, previous_xy_xor_output_var, "AND"}

    a1, a2, b1 = None, None, None
    for top in target_influence_operations:
        left_side_vars = set(top[:-1])
        if left_side_vars == a1_vars:
            a1 = top[-1]
        elif left_side_vars == a2_vars:
            a2 = top[-1]
        elif left_side_vars == b1_vars:
            b1 = top[-1]

    assert a1 is not None
    assert a2 is not None
    assert b1 is not None

    c1_vars = {b1, a1, "OR"}
    c1 = None
    for top in target_influence_operations:
        left_side_vars = set(top[:-1])
        if left_side_vars == c1_vars:
            c1 = top[-1]

    assert c1 is not None

    z_vars = {c1, a2, "XOR"}
    z = None
    for top in target_influence_operations:
        left_side_vars = set(top[:-1])
        if left_side_vars == z_vars:
            z = top[-1]

    if z is None:
        possible_changes = []
        for other_op in operations:
            left_side_vars = set(other_op[:-1])
            if left_side_vars == z_vars:
                possible_changes.append(other_op)
        swap_op = possible_changes[0]
        operations.remove(swap_op)

        # now lets find the operation ending in z = target
        possible_changes = []
        for other_op in operations:
            if other_op[-1] == target:
                possible_changes.append(other_op)
        zswap = possible_changes[0]
        operations.remove(zswap)

        new_zop = swap_op[:-1] + (target,)
        new_sop = zswap[:-1] + (swap_op[-1],)

        operations.append(new_zop)
        operations.append(new_sop)
        return [target, swap_op[-1]]


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

    fixed = [8]
    swapped_wires = []
    for idx in fixed:
        swp = complete_vars_for_z(idx, z_sets, operations)
        if isinstance(swp, list):
            swapped_wires += swp
    # wanted_index = 4
    # while wanted_index < N:
    #     print(wanted_index)
    #     complete_vars_for_z(wanted_index, z_sets, operations)
    #     wanted_index += 1

    # sys.exit()

    wanted_index = 9
    target = f"z{str(wanted_index).zfill(2)}"
    previous = f"z{str(wanted_index-1).zfill(2)}"
    previous_previous = f"z{str(wanted_index-2).zfill(2)}"

    target_influence_operations = find_operations_from_vars(
        z_sets[target] - z_sets[previous], operations
    )
    for o in target_influence_operations:
        print(o)
    previous_influence_operations = find_operations_from_vars(
        z_sets[previous] - z_sets[previous_previous], operations
    )

    previous_x = get_wire_string("x", wanted_index - 1)
    previous_y = get_wire_string("y", wanted_index - 1)
    previous_or_output_var = None
    previous_xy_xor_output_var = None
    for top in previous_influence_operations:
        if top[1] == "OR":
            previous_or_output_var = top[-1]
        if set(top[:-1]) == {previous_x, previous_y, "XOR"}:
            previous_xy_xor_output_var = top[-1]

    print(previous_or_output_var, previous_xy_xor_output_var)

    target_x = get_wire_string("x", wanted_index)
    target_y = get_wire_string("y", wanted_index)
    a1_vars = {previous_x, previous_y, "AND"}
    a2_vars = {target_x, target_y, "XOR"}
    b1_vars = {previous_or_output_var, previous_xy_xor_output_var, "AND"}

    a1, a2, b1 = None, None, None
    for top in target_influence_operations:
        left_side_vars = set(top[:-1])
        if left_side_vars == a1_vars:
            a1 = top[-1]
        elif left_side_vars == a2_vars:
            a2 = top[-1]
        elif left_side_vars == b1_vars:
            b1 = top[-1]

    c1_vars = {b1, a1, "OR"}
    c1 = None
    for top in target_influence_operations:
        left_side_vars = set(top[:-1])
        if left_side_vars == c1_vars:
            c1 = top[-1]

    z_vars = {c1, a2, "XOR"}
    z = None
    for top in target_influence_operations:
        left_side_vars = set(top[:-1])
        if left_side_vars == z_vars:
            z = top[-1]
    print(a1, b1, a2, c1, z)
