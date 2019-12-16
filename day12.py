# pylint: disable=C0114, C0115, C0116, C0103, R0914
from dataclasses import dataclass
from utils import get_input, sscanf, gcd

@dataclass
class Position:
    x: int
    y: int
    z: int


@dataclass
class Velocity:
    x: int
    y: int
    z: int


@dataclass
class Moon:
    pos: Position
    vel: Velocity


DATA = get_input(12)
# DATA = [r"<x=-1, y=0, z=2>", r"<x=2, y=-10, z=-7>", r"<x=4, y=-8, z=8>", r"<x=3, y=5, z=-1>"]
# DATA = [r"<x=-8, y=-10, z=0>", r"<x=5, y=5, z=10>", r"<x=2, y=-7, z=3>", r"<x=9, y=-8, z=-3>"]
RGX = r"x=(-?\d+), y=(-?\d+), z=(-?\d+)"


def init(data):
    return [Moon(Position(*sscanf(t, RGX, [int]*3)), Velocity(0, 0, 0)) for t in data]

def apply_gravity(moons):
    for moon in moons:
        for other_moon in moons:
            if moon.pos.x < other_moon.pos.x:
                moon.vel.x += 1
            elif moon.pos.x > other_moon.pos.x:
                moon.vel.x -= 1
            if moon.pos.y < other_moon.pos.y:
                moon.vel.y += 1
            elif moon.pos.y > other_moon.pos.y:
                moon.vel.y -= 1
            if moon.pos.z < other_moon.pos.z:
                moon.vel.z += 1
            elif moon.pos.z > other_moon.pos.z:
                moon.vel.z -= 1


def apply_velocity(moons):
    for moon in moons:
        moon.pos.x += moon.vel.x
        moon.pos.y += moon.vel.y
        moon.pos.z += moon.vel.z


def part1():
    moons = init(DATA)
    for _ in range(1000):
        apply_gravity(moons)
        apply_velocity(moons)
    # print(f"\nAfter {_+1} steps:")
    # for moon in moons:
    #     print(f"{moon.pos}, {moon.vel}")
    # print(f"Energy after {_+1} steps:")
    acc = 0
    for moon in moons:
        pot = abs(moon.pos.x) + abs(moon.pos.y) + abs(moon.pos.z)
        kin = abs(moon.vel.x) + abs(moon.vel.y) + abs(moon.vel.z)
        tot = pot * kin
        acc += tot
    #     print(f"{pot=}, {kin=}, {tot=}")
    # print(f"{acc=}")
    return acc


def part2():
    """."""
    moons = init(DATA)
    x = 0
    seen = set()
    while True:
        apply_gravity(moons)
        apply_velocity(moons)
        s = ""
        for moon in moons:
            s += "{},{},".format(moon.pos.x, moon.vel.x)
        if s in seen:
            break
        x += 1
        seen.add(s)
    moons = init(DATA)
    y = 0
    seen = set()
    while True:
        apply_gravity(moons)
        apply_velocity(moons)
        s = ""
        for moon in moons:
            s += "{},{},".format(moon.pos.y, moon.vel.y)
        if s in seen:
            break
        y += 1
        seen.add(s)
    moons = init(DATA)
    z = 0
    seen = set()
    while True:
        apply_gravity(moons)
        apply_velocity(moons)
        s = ""
        for moon in moons:
            s += "{},{},".format(moon.pos.z, moon.vel.z)
        if s in seen:
            break
        z += 1
        seen.add(s)
    return int(x*y*z / 16)

if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}\n")
    print(f"\n    Part 2\n    {part2()}\n")
