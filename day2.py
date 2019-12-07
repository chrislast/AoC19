# pylint: disable=C0114, C0116, C0103
from utils import get_input, IntcodeComputer

DATA = get_input(2)

PROGRAM = list(map(int, DATA[0].split(',')))
# print(PROGRAM)


def part1():
    """."""
    prog = PROGRAM[:]
    computer = IntcodeComputer(prog, 12, 2)
    computer.execute()
    return prog[0]


def part2():
    for n in range(100):
        for v in range(100):
            prog = PROGRAM[:]
            computer = IntcodeComputer(prog, n, v)
            computer.execute()
            if prog[0] == 19690720:
                return n * 100 + v
    return None


print(f"\n    Part 1\n    {part1()}")
print(f"\n    Part 2\n    {part2()}")

assert part1() == 5290681
assert part2() == 5741
