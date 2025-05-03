from pathlib import Path


def read_input(file: str):
    data = Path(file).read_text()
    available, combinations = data.split("\n\n")

    available_options = available.split(", ")
    wanted_combinations = combinations.splitlines()
    return available_options, wanted_combinations


if __name__ == "__main__":
    import sys

    _filename = sys.argv[1]
    filename = f"{_filename}.txt"

    available, wanted = read_input(filename)

    print(available)
    print(wanted)

    wanted_word = wanted[0]
    # next_available = []
    possibles = []
    for wanted_word in wanted:
        current_words = [wanted_word]
        full_match = False
        while len(current_words) > 0:
            some_matched = False
            next_words = []
            for current_word in current_words:
                for option in available:
                    if current_word.startswith(option):
                        some_matched = True
                        nw = current_word.removeprefix(option)
                        next_words.append(nw)
                        if len(nw) == 0:
                            full_match = True

            current_words = next_words
            if full_match:
                possibles.append(wanted_word)
                break
    print(len(possibles), possibles)
