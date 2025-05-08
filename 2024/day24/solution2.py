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


def complete_vars_for_z(
    wanted_index: int, z_sets: dict, operations: list, swapped: list
):
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
    previous_c1 = None
    previous_a1 = None
    for top in previous_influence_operations:
        if top[1] == "OR":
            previous_c1 = top[-1]
        if set(top[:-1]) == {previous_x, previous_y, "XOR"}:
            previous_a1 = top[-1]

    target_x = get_wire_string("x", wanted_index)
    target_y = get_wire_string("y", wanted_index)
    a1_vars = {target_x, target_y, "XOR"}
    a2_vars = {previous_x, previous_y, "AND"}
    b1_vars = {previous_c1, previous_a1, "AND"}

    a1, a2, b1 = None, None, None
    for top in target_influence_operations:
        left_side_vars = set(top[:-1])
        if left_side_vars == a1_vars:
            a1 = top[-1]
        elif left_side_vars == a2_vars:
            a2 = top[-1]
        elif left_side_vars == b1_vars:
            b1 = top[-1]

    # assert a1 is not None
    # assert a2 is not None
    # assert b1 is not None

    c1_vars = {b1, a2, "OR"}
    c1 = None
    for top in target_influence_operations:
        left_side_vars = set(top[:-1])
        if left_side_vars == c1_vars:
            c1 = top[-1]

    # assert c1 is not None

    z_vars = {c1, a1, "XOR"}
    z = None
    for top in target_influence_operations:
        left_side_vars = set(top[:-1])
        if left_side_vars == z_vars:
            z = top[-1]

    return {
        "a1": a1,
        "a2": a2,
        "b1": b1,
        "c1": c1,
        "z": z
    }

    if z is None:
        target_wire = target
        target_left_vars = z_vars

        swapped_wires = swap_outputs_z(target_wire, target_left_vars, operations)
        swapped += swapped_wires


def swap_outputs_z(target_wire: str, target_left_vars: set, operations: list):
    # find the other wire
    possible_changes = []
    for other_op in operations:
        left_side_vars = set(other_op[:-1])
        if left_side_vars == target_left_vars:
            possible_changes.append(other_op)
    to_swap_op = possible_changes[0]
    operations.remove(to_swap_op)

    # now lets find the operation ending in z = target
    possible_changes = []
    for other_op in operations:
        if other_op[-1] == target_wire:
            possible_changes.append(other_op)
    target_swap = possible_changes[0]
    operations.remove(target_swap)

    n1 = to_swap_op[:-1] + (target_wire,)
    n2 = target_swap[:-1] + (to_swap_op[-1],)

    operations.append(n1)
    operations.append(n2)
    return [target_wire, to_swap_op[-1]]


def is_valid(wanted_index: int, z_sets: dict, operations: list) -> bool:
    target_z = get_wire_string("z", wanted_index)
    previous_z = get_wire_string("z", wanted_index - 1)
    previous_previous_z = get_wire_string("z", wanted_index - 2)

    previous_influence_operations = find_operations_from_vars(
        z_sets[previous_z] - z_sets[previous_previous_z], operations
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
    a1 = None
    for top in operations:
        if set(top[:-1]) == a1_vars:
            a1 = top[-1]
            break

    # lets find a2
    a2_vars = {previous_x, previous_y, "AND"}
    a2 = None
    for top in operations:
        if set(top[:-1]) == a2_vars:
            a2 = top[-1]
            break

    # lets find b1
    b1_vars = {previous_c1, previous_a1, "AND"}
    b1 = None
    for top in operations:
        if set(top[:-1]) == b1_vars:
            b1 = top[-1]
            break

    # lets find c1
    c1_vars = {b1, "OR", a2}
    c1 = None
    for top in operations:
        if set(top[:-1]) == c1_vars:
            c1 = top[-1]
            break

    # so now lets find the c1 XOR a1 that should produce z
    c1_xor_a1_vars = {c1, "XOR", a1}
    c1_xor_a1_out = None
    for top in operations:
        if set(top[:-1]) == c1_xor_a1_vars:
            c1_xor_a1_out = top[-1]
            break

    return c1_xor_a1_out == target_z, previous_a1, previous_c1

def get_op_from_vars(vars: str, operations: list):
    for op in operations:
        if set(op[:-1]) == vars:
            return op
    return None

def get_op_from_out(out: str, operations: list):
    for op in operations:
        if op[-1] == out:
            return op
    return None

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

    for idx in reversed(range(0, 12)):
        valid, previous_a1, previous_c1 = is_valid(idx, z_sets, operations)
        if not valid:
            print(idx)
            break
        a1, c1 = previous_a1, previous_c1
        print("VALID", idx, a1, c1)


    # lets find if z is correct
    target_z = get_wire_string("z", idx)
    z_vars = {c1, "XOR", a1}
    _op = get_op_from_vars(z_vars, operations)
    _op_out = _op[-1]
    print(target_z, _op)
    assert target_z == _op_out # TODO: change if not

    c1_op = get_op_from_out(c1, operations)
    possibles_a2 = {c1_op[0], c1_op[2]}
    possibles_b1 = {c1_op[0], c1_op[2]}
    print(possibles_a2)
    
    previous_x = get_wire_string("x", idx-1)
    previous_y = get_wire_string("y", idx-1)
    
    a2_vars = {previous_x, "AND", previous_y}
    a2_op = get_op_from_vars(a2_vars, operations)
    a2_op_out = a2_op[-1]
    assert a2_op_out in possibles_a2 # TODO: deal if not
    a2 = a2_op_out

    b1 = list(possibles_b1 - {a2})[0]
    b1_op = get_op_from_out(b1, operations)
    print(b1_op)

    
    
