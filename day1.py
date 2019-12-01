from utils import get_input, run
from math import floor

DATA = get_input(1, int)


def _f1():
    pass

def _part1():
    return sum([floor(v / 3) - 2 for v in DATA])

def _fuel(mass):
    extra = floor(mass / 3) - 2
    if extra < 1:
        return 0
    return extra + _fuel(extra)

def _part2():
    return sum([_fuel(v) for v in DATA])

run(_part1, _part2)
