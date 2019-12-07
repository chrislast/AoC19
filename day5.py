# pylint: disable=C0114, C0116, C0103
from utils import get_input, IntcodeComputer

DATA = get_input(5)

PROGRAM = list(map(int, DATA[0].split(',')))
# print(PROGRAM)


def part1():
    """."""
    prog = PROGRAM[:]
    computer = IntcodeComputer(prog, input_fifo=[1])
    return computer.execute()[-1]


def part2():
    prog = PROGRAM[:]
    computer = IntcodeComputer(prog, input_fifo=[5])
    return computer.execute()[-1]


res = part1()
print(f"\n    Part 1\n    {res}\n")
assert res == 13346482

res = part2()
print(f"\n    Part 2\n    {res}\n")
assert res == 12111395
