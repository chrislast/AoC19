# pylint: disable=C0114, C0116, W0611
from math import floor
from utils import get_input

DATA = get_input(1, int)


def part1():
    return sum([floor(v/3)-2 for v in DATA])


def fuel(mass):
    extra = floor(mass/3)-2
    if extra < 1:
        return 0
    return extra + fuel(extra)


def part2():
    return sum([fuel(v) for v in DATA])


if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}")
    print(f"\n    Part 2\n    {part2()}")
