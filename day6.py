# pylint: disable=C0114, C0116, C0103
from utils import get_input, IntcodeComputer

DATA = get_input(6)

ORBITS = dict()

def part1():
    for orbit in DATA:
        ctr, orb = orbit.split(')')
        ORBITS[orb] = ctr
    acc = 0
    # import pdb; pdb.set_trace()
    for orb in ORBITS:
        acc += 1
        centre = ORBITS[orb]
        while centre != 'COM':
            acc += 1
            centre = ORBITS[centre]
    return acc

def get_path(start):
    acc = start
    par = ORBITS[start]
    while par != "COM":
        acc = par + ")" + acc
        par = ORBITS[par]
    return par + ")" + acc

def part2():
    youpath = get_path("YOU")[:-3]
    sanpath = get_path("SAN")[:-3]
    while youpath[:4] == sanpath[:4]:
        youpath = youpath[4:]
        sanpath = sanpath[4:]
    return int(len(youpath)/4 + len(sanpath)/4)

res = part1()
print(f"\n    Part 1\n    {res}\n")
assert res == 268504

res = part2()
print(f"\n    Part 2\n    {res}\n")
assert res == 409
