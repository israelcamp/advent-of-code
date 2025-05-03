from pathlib import Path


def read_input(file: str):
    data = Path(file).read_text()
    available, combinations = data.split("\n\n")

    available_options = available.split(", ")
    wanted_combinations = combinations.splitlines()
    return available_options, wanted_combinations


def solution_part_one(available, wanted):
    possibles = []
    for wanted_word in wanted:
        current_words = {wanted_word}
        full_match = False
        while len(current_words) > 0:
            next_words = set()
            for current_word in current_words:
                for option in available:
                    if current_word.startswith(option):
                        nw = current_word.removeprefix(option)
                        if len(nw) == 0:
                            full_match = True
                        else:
                            next_words.add(nw)

            current_words = next_words.copy()
            if full_match:
                possibles.append(wanted_word)
                break
    return len(possibles)


def n_ways_to_solve(target: str, available: list[str], memo: dict) -> int:

    if target in memo:
        return memo[target]

    result = 0
    for option in available:
        if not target.endswith(option):
            continue

        next_target = target.removesuffix(option)
        if next_target == "":  ## matched
            result += 1

        r = n_ways_to_solve(next_target, available, memo)
        result += r
    memo[target] = result

    return result


if __name__ == "__main__":
    import sys

    _filename = sys.argv[1]
    filename = f"{_filename}.txt"

    available, wanted = read_input(filename)

    possibles = solution_part_one(available, wanted)

    print("RESULT PART ONE", possibles)

    memo = {}
    result = 0
    for wanted_word in wanted:
        result += n_ways_to_solve(wanted_word, available, memo)

    print("RESULT PART TWO", result)
