# pylint: disable=C0114, C0116, C0103
from utils import get_input, IntcodeComputer
from itertools import permutations

DATA = get_input(7)

PROGRAM = list(map(int, DATA[0].split(',')))
# print(PROGRAM)
PERMS = permutations(range(5))
PERMS2 = permutations(range(5, 10))


def part1():
    """."""
    best = 0
    for a, b, c, d, e in PERMS:
        ampa = IntcodeComputer(PROGRAM, input_fifo=[a, 0])
        ampb = IntcodeComputer(PROGRAM, input_fifo=[b, ampa.execute()])
        ampc = IntcodeComputer(PROGRAM, input_fifo=[c, ampb.execute()])
        ampd = IntcodeComputer(PROGRAM, input_fifo=[d, ampc.execute()])
        ampe = IntcodeComputer(PROGRAM, input_fifo=[e, ampd.execute()])
        res = ampe.execute()
        if res > best:
            best = res
    return best


def part2():
    best = 0
    for a, b, c, d, e in PERMS2:
        ampa = IntcodeComputer(PROGRAM, input_fifo=[a], signals=True)
        ampb = IntcodeComputer(PROGRAM, input_fifo=[b], signals=True)
        ampc = IntcodeComputer(PROGRAM, input_fifo=[c], signals=True)
        ampd = IntcodeComputer(PROGRAM, input_fifo=[d], signals=True)
        ampe = IntcodeComputer(PROGRAM, input_fifo=[e], signals=True)
        val = 0
        while not ampe.done:
            for amp in (ampa, ampb, ampc, ampd, ampe):
                amp.add_input(val)
                val = amp.execute()
        if val > best:
            best = val
    return best


if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}\n")
    print(f"\n    Part 2\n    {part2()}\n")
