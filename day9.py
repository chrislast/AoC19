# pylint: disable=C0114, C0116, C0103
from utils import get_input, IntcodeComputer

DATA = get_input(9)

PROGRAM = list(map(int, DATA[0].split(',')))


def part1():
    """."""
    computer = IntcodeComputer(PROGRAM, input_fifo=[1])
    computer.execute()
    return computer.output_data[-1]


def part2():
    computer = IntcodeComputer(PROGRAM, input_fifo=[2])
    computer.execute()
    return computer.output_data[-1]


if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}\n")
    print(f"\n    Part 2\n    {part2()}\n")
