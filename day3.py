# pylint: disable=C0114, C0116, C0103
from utils import get_input, IntcodeComputer

DATA = get_input(3)


def add(x, y, l, step):
    dirn = step[0]
    steps = int(step[1:])
    for _ in range(steps):
        if dirn == "U":
            y += 1
        elif dirn == "D":
            y -= 1
        if dirn == "L":
            x -= 1
        elif dirn == "R":
            x += 1
        l.add((x, y))
    return x, y


def part1():
    """."""
    wires = []
    for wireplan in DATA:
        wires.append(set())
        x = y = 0
        for step in wireplan.split(','):
            x, y = add(x, y, wires[-1], step)
    res = wires[0] & wires[1]
    dist = [abs(x)+abs(y) for x, y in res]
    return min(dist)


def add2(x, y, l, m, n, step):
    dirn = step[0]
    steps = int(step[1:])
    for _ in range(steps):
        if dirn == "U":
            y += 1
        elif dirn == "D":
            y -= 1
        if dirn == "L":
            x -= 1
        elif dirn == "R":
            x += 1
        l.add((x, y))
        n += 1
        if ((x,y) not in m):
            m[(x,y)] = n
    return x, y, n


def part2():
    """."""
    wires = []
    stepcount = []
    for wireplan in DATA:
        wires.append(set())
        stepcount.append(dict())
        x = y = n = 0
        for step in wireplan.split(','):
            x, y, n = add2(x, y, wires[-1], stepcount[-1], n, step)
    res = wires[0] & wires[1]
    dist = [stepcount[0][(x,y)]+stepcount[1][(x,y)] for x, y in res]
    return min(dist)


if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}")
    print(f"\n    Part 2\n    {part2()}")
