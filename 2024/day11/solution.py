from pathlib import Path

def read_input(file: str) -> list[int]:
    data = Path(file).read_text()
    return [int(l) for l in data.split()]

def update_stone(stone: int) -> list[int]:
    new_stones = []
    if stone == 0:
        stone = 1
        new_stones.append(stone)
    elif len(str(stone)) % 2 == 0:
        string_stone = str(stone)
        n = len(string_stone) // 2
        left = string_stone[:n]
        right = string_stone[n:]
        new_stones.append(int(left))
        new_stones.append(int(right))
    else:
        new_stones.append(2024 * stone)
    return new_stones

def count_children(stone: int, step: int, max_steps: int, memo: dict) -> int:

    if (stone, step) in memo:
        return memo[(stone, step)]
    
    next_stones = update_stone(stone)

    if step + 1 == max_steps:
        return len(next_stones)
    
    result = 0
    for st in next_stones:
        result += count_children(st, step + 1, max_steps, memo)
    
    memo[(stone, step)] = result

    return result
    


if __name__ == "__main__":
    file = "./input.txt"
    stones = read_input(file)

    blinks = 75

    memo = {}
    result = 0
    for current_stone in stones:
        r = count_children(current_stone, 0, blinks, memo)
        result += r

    print(result)

