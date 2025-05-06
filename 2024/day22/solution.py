from pathlib import Path
from collections import defaultdict


def read_input(file: str) -> list[int]:
    return [int(x) for x in Path(file).read_text().splitlines()]


def evolve_number(secret_number: int) -> int:
    number = secret_number * 64
    secret_number = secret_number ^ number
    secret_number = secret_number % 16777216

    number = secret_number // 32
    secret_number = secret_number ^ number
    secret_number = secret_number % 16777216

    number = secret_number * 2048
    secret_number = secret_number ^ number
    secret_number = secret_number % 16777216

    return secret_number


if __name__ == "__main__":
    import sys

    filename = f"{sys.argv[1]}.txt"
    max_iterations = int(sys.argv[2])

    secrets = read_input(filename)

    result = 0
    prices_per_secret = defaultdict(list)
    changes_per_secret = defaultdict(list)
    for initial_secret in secrets:
        secret_number = initial_secret
        current_price = int(str(secret_number)[-1])
        for _ in range(max_iterations):
            secret_number = evolve_number(secret_number)
            price = int(str(secret_number)[-1])
            change = price - current_price

            prices_per_secret[initial_secret].append(price)
            changes_per_secret[initial_secret].append(change)

            current_price = price

        result += secret_number

    print("SUM", result)
    assert len(changes_per_secret) == len(secrets)

    start, end = 0, 4
    sequences_to_secrets = defaultdict(dict)
    N = len(changes_per_secret[initial_secret])

    while end < N:
        for secret in secrets:
            current_sequence = tuple(changes_per_secret[secret][start:end])
            current_value = prices_per_secret[secret][end - 1]

            # already saw this sequence for this secret
            if secret in sequences_to_secrets[current_sequence]:
                continue

            sequences_to_secrets[current_sequence][secret] = current_value

        start += 1
        end += 1

    best_sequence, best_value = None, -1_000_00
    for sequence, secret_to_values in sequences_to_secrets.items():
        sequence_total = sum([v for v in secret_to_values.values()])
        if sequence_total > best_value:
            best_sequence = sequence
            best_value = sequence_total

    print(best_sequence, best_value)
