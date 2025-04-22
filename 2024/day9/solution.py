from pathlib import Path


def read_input(file: str) -> list[int]:
    data = Path(file).read_text()
    return list([int(x) for x in data])


def solution_part_one(blocks: list[str]) -> int:
    left, right = 0, len(blocks) - 1

    while True:
        while blocks[left] != ".":
            left += 1

        while blocks[right] == ".":
            right -= 1

        if left >= len(blocks) or right < 0 or right <= left:
            break

        blocks[left], blocks[right] = blocks[right], blocks[left]
        left += 1
        right -= 1

    result = 0
    for i, v in enumerate(blocks):
        if v == ".":
            break
        result += int(v) * i

    return result


if __name__ == "__main__":
    file = "./input.txt"
    data = read_input(file)

    _id = 0
    is_free_space = False
    blocks = []
    for mem_count in data:
        value = "." if is_free_space else str(_id)
        blocks += [value] * mem_count
        is_free_space = not is_free_space
        _id = _id if is_free_space else _id + 1

    result_part_one = solution_part_one(blocks.copy())

    left, right = 0, len(blocks) - 1
    current_id = None

    ## find first id
    current_id = blocks[right]
    current_file_block_size = 0
    while current_id == ".":
        right -= 1
        current_id = blocks[right]

    ## find the first free space

    while True:
        current_file_block_size = 0
        while blocks[right] != current_id:
            right -= 1

        # find the current block of ids to move
        while blocks[right] == current_id and right > 0:
            current_file_block_size += 1
            right -= 1

        left = 0
        current_free_space_size = 0
        # find the block of free space that fits the current block
        while left <= right:
            if blocks[left] == ".":
                current_free_space_size += 1
            else:
                current_free_space_size = 0

            if current_free_space_size == current_file_block_size:
                swap_size = current_file_block_size
                blocks[left + 1 - swap_size : left + 1] = [current_id] * swap_size
                blocks[right + 1 : right + 1 + swap_size] = ["."] * swap_size
                break

            left += 1

        next_id = int(current_id) - 1
        if next_id < 0:
            break
        current_id = str(next_id)

    result = 0
    for i, v in enumerate(blocks):
        if v == ".":
            continue
        result += int(v) * i

    print("PART ONE", result_part_one)
    print("PART TWO", result)
