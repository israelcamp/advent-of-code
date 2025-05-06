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

if __name__ == "__main__":
    import sys

    filename = f"{sys.argv[1]}.txt"
    known_values, operations = read_input(filename)

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

    zvalues = {}
    for key, value in known_values.items():
        if not key.startswith("z"):
            continue
        power = int(key[1:])
        zvalues[power] = value

    power = 0
    result = 0
    while power in zvalues:
        result += zvalues[power] * (2**power)
        power += 1

    print(result)
