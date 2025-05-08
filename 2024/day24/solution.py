from pathlib import Path


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


def solution_part_one(known_values, operations):
    update_known_values(known_values, operations)

    result = 0
    for key, value in known_values.items():
        if not key.startswith("z"):
            continue
        power = int(key[1:])
        result += value * (2**power)

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


if __name__ == "__main__":
    import sys

    filename = f"{sys.argv[1]}.txt"
    known_values, operations = read_input(filename)

    x_string_result = ""
    x_value_result = 0
    y_string_result = ""
    y_value_result = 0

    power = 0
    xn = f"x{str(power).zfill(2)}"
    yn = f"y{str(power).zfill(2)}"
    while xn in known_values and yn in known_values:
        xs = known_values[xn]
        ys = known_values[yn]

        x_string_result = str(xs) + x_string_result
        y_string_result = str(ys) + y_string_result

        x_value_result += xs * (2**power)
        y_value_result += ys * (2**power)

        power += 1
        xn = f"x{str(power).zfill(2)}"
        yn = f"y{str(power).zfill(2)}"

    z_value_result = x_value_result + y_value_result
    z_string_result = f"{z_value_result:b}"
    print(x_string_result, x_value_result, y_string_result, y_value_result)
    print(z_value_result, z_string_result)

    wanted_z_values = {}
    for i, v in enumerate(reversed(z_string_result)):
        zs = f"z{str(i).zfill(2)}"
        wanted_z_values[zs] = v

    print(wanted_z_values)

    solved_known_values = known_values.copy()
    result = solution_part_one(solved_known_values, operations)

    print(solved_known_values)

    for key, value in wanted_z_values.items():
        solved = solved_known_values.get(key, -1)
        if int(solved) != int(value):
            print("BAD")
        print(key, "wanted", value, "solved", solved_known_values.get(key, "-"))

    target_z = "z08"
    target_vars = []
    for op_ in operations:
        var1, op, var2, out = op_
        if out != target_z:
            continue
        target_vars.append(var1)
        target_vars.append(var2)
        print(op_)

    print(target_vars)

    next_target_vars = []
    for op_ in operations:
        var1, op, var2, out = op_
        if out not in target_vars:
            continue

        print(op_)

        next_target_vars.append(var1)
        next_target_vars.append(var2)

    contains_x = any([v.startswith("x") for v in next_target_vars])
    contains_y = any([v.startswith("y") for v in next_target_vars])

    print(next_target_vars)
