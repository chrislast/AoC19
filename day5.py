# pylint: disable=C0114, C0116, C0103
from utils import get_input, IntcodeComputer

DATA = get_input(5)

PROGRAM = list(map(int, DATA[0].split(',')))


def part1():
    """."""
    computer = IntcodeComputer(PROGRAM, input_fifo=[1])
    return computer.execute()


def part2():
    computer = IntcodeComputer(PROGRAM, input_fifo=[5])
    return computer.execute()


if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}\n")
    print(f"\n    Part 2\n    {part2()}\n")
