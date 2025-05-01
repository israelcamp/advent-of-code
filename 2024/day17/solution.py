from dataclasses import dataclass
from pathlib import Path
import re


def read_input(file: str):
    data = Path(file).read_text()
    numbers = [int(x) for x in re.findall(r"-?[0-9]{1,}", data)]
    A, B, C, *instructions = numbers
    return Register(A=A, B=B, C=C), instructions


@dataclass
class Register:
    A: int = -1
    B: int = -1
    C: int = -1


def get_value_from_operand(operand: int, register: Register) -> int:
    if 0 <= operand < 4:
        return operand
    if operand == 4:
        return register.A
    if operand == 5:
        return register.B
    if operand == 6:
        return register.C
    raise ValueError("no value for operand")


def opcode0_adv(combo: int, literal: int, register: Register) -> None:
    result = int(register.A / (2**combo))
    register.A = result


def opcode1_bxl(combo: int, literal: int, register: Register):
    register.B = register.B ^ literal


def opcode2_bst(combo: int, literal: int, register: Register):
    register.B = combo % 8


def opcode4_bxc(combo: int, literal: int, register: Register):
    register.B = register.B ^ register.C


def opcode5_out(combo: int, literal: int, register: Register) -> int:
    return combo % 8


def opcode6_bdv(combo: int, literal: int, register: Register):
    result = int(register.A / (2**combo))
    register.B = result


def opcode7_cdv(combo: int, literal: int, register: Register):
    result = int(register.A / (2**combo))
    register.C = result


def opcode3_jnz(combo: int, literal: int, register: Register):
    return


def decide_operator(operation: int):
    if operation == 0:
        return opcode0_adv
    if operation == 1:
        return opcode1_bxl
    if operation == 2:
        return opcode2_bst
    if operation == 3:
        return opcode3_jnz
    if operation == 4:
        return opcode4_bxc
    if operation == 5:
        return opcode5_out
    if operation == 6:
        return opcode6_bdv
    if operation == 7:
        return opcode7_cdv


def solution_part_one(register: Register, program: list[int]) -> list[int]:
    pointer = 0
    outs = []
    while pointer < len(program):
        commands = program[pointer : pointer + 2]

        operation, operand = commands

        if operation == 3 and register.A != 0:
            pointer = operand
            continue

        combo = get_value_from_operand(operand, register)
        operation = decide_operator(operation)
        result = operation(combo, operand, register)
        if result is not None:
            outs.append(result)

        pointer += 2
    return outs


if __name__ == "__main__":
    import sys

    filename = sys.argv[1]
    file = f"{filename}.txt"

    _, program = read_input(file)

    A = 0
    for idx, target_output in enumerate(reversed(program)):
        A *= 8
        reg = Register(A=A, B=0, C=0)
        offset = 0
        while solution_part_one(reg, program) != program[-idx - 1 :]:
            A += 1
            reg = Register(A=A, B=0, C=0)

    print(A)
    print(solution_part_one(Register(A=A, B=0, C=0), program))
    print(program)
