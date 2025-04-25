from pathlib import Path
import re
from dataclasses import dataclass


@dataclass
class Button:
    dx: int
    dy: int


@dataclass
class Game:
    a: Button
    b: Button
    x: int
    y: int


def read_input(file: str) -> list[Game]:
    data = Path(file).read_text()
    games = []
    for game_data in data.split("\n\n"):
        numbers = [int(x) for x in re.findall(r"[0-9]{1,}", game_data)]
        adx, ady, bdx, bdy, x, y = numbers
        games.append(Game(a=Button(dx=adx, dy=ady), b=Button(dx=bdx, dy=bdy), x=x, y=y))
    return games


if __name__ == "__main__":
    file = "./sample.txt"
    games = read_input(file)

    current_game = games[0]

    # na * a.dx + nb * b.dx = x
    # na * a.dy + nb * b.dy = y
    # na * (a.dx - a.dy) + nb * (b.dx - b.dy) = x - y

    print(games)
