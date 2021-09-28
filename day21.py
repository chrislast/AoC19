# pylint: disable=C0114, C0116, C0103, R0914
from utils import get_input, IntcodeComputer, bfs, TRACE, TEXT
import re

DATA = get_input(21)
PROGRAM = list(map(int, DATA[0].split(',')))

ANSWER1 = """NOT B J
NOT C T
OR T J
AND D J
NOT A T
OR T J
WALK
"""

ANSWER2 = """NOT B J
NOT C T
OR T J
AND D J
AND H J
NOT A T
OR T J
RUN
"""

def part1():
    computer = IntcodeComputer(PROGRAM, input_fifo=ANSWER1, mode=TEXT)
    ans = computer.execute()
    return int(ans)

def part2():
    computer = IntcodeComputer(PROGRAM, input_fifo=ANSWER2, mode=TEXT)
    ans = computer.execute()
    return int(ans)

if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}\n")
    print(f"\n    Part 2\n    {part2()}\n")
