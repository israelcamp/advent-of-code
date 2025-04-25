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

A_PRICE = 3
B_PRICE = 1


def read_input(file: str) -> list[Game]:
    data = Path(file).read_text()
    games = []
    for game_data in data.split("\n\n"):
        numbers = [int(x) for x in re.findall(r"[0-9]{1,}", game_data)]
        adx, ady, bdx, bdy, x, y = numbers
        games.append(Game(a=Button(dx=adx, dy=ady), b=Button(dx=bdx, dy=bdy), x=x, y=y))
    return games

def solve_game(game: Game) -> int:
    a = game.a
    b = game.b

    left_side = a.dx - a.dy - (a.dx / b.dx) * (b.dx - b.dy)
    right_side = game.x - game.y - (game.x / b.dx) * (b.dx - b.dy)

    na = right_side / left_side
    nb = (game.x - na * a.dx) / (b.dx)

    if na < 0 or nb < 0:
        return 0
    
    rounded_a, rounded_b = round(na), round(nb)
    is_a_close = abs(rounded_a - na) < 1e-3
    is_b_close = abs(rounded_b - nb) < 1e-3

    if not is_a_close or not is_b_close:
        return 0
    
    return rounded_a * A_PRICE + rounded_b * B_PRICE


if __name__ == "__main__":
    file = "./input.txt"
    games = read_input(file)

    result = 0
    for game in games:
        r = solve_game(game)
        result += r

    print("PART ONE", int(result))

    result = 0
    for game in games:
        game.x = 10000000000000 + game.x
        game.y = 10000000000000 + game.y
        r = solve_game(game)
        result += r

    print("PART TWO", int(result))