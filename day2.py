# pylint: disable=C0114, C0116, C0103
from utils import get_input, IntcodeComputer

DATA = get_input(2)

PROGRAM = list(map(int, DATA[0].split(',')))
# print(PROGRAM)


def part1():
    """."""
    computer = IntcodeComputer(PROGRAM, 12, 2)
    computer.execute()
    return computer.program[0]


def part2():
    for n in range(100):
        for v in range(100):
            computer = IntcodeComputer(PROGRAM, n, v)
            computer.execute()
            if computer.program[0] == 19690720:
                return n * 100 + v
    return None


if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}")
    print(f"\n    Part 2\n    {part2()}")

