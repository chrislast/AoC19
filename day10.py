# pylint: disable=C0114, C0116, C0103
from collections import Counter, namedtuple
from utils import get_input
import math

DATA = get_input(10)
HEIGHT = len(DATA)
WIDTH = len(DATA[0])

ASTEROIDS = tuple((x, y) for x in range(WIDTH) for y in range(HEIGHT) if DATA[y][x] == "#")

STATION = None

def angles(base_x, base_y):
    res = set()
    for x, y in ASTEROIDS:
        if base_x == x and base_y == y:
            continue
        res.add(
            math.degrees(math.atan2(x-base_x, -(y-base_y))))
    return res

def part1():
    # for each empty space
    stations = dict()
    for x, y in ASTEROIDS:
        stations[(x, y)] = len(angles(x, y))
    global STATION
    STATION = max(stations, key=stations.get)
    return stations[STATION]


def anglerange(base_x, base_y):
    res = dict()
    for x, y in ASTEROIDS:
        if base_x == x and base_y == y:
            continue
        # (asteroid x, asteroid y): (angle to asteroid, range to asteroid)
        res[(x, y)] = (
            math.degrees(math.atan2(x-base_x, -(y-base_y))),
            (abs(y-base_y)**2 + abs(x-base_x)**2)**0.5)
    return res

def part2():
    # for each empty space
    x, y = STATION
    asteroids = anglerange(*STATION)
    laser_angle = -0.0000001
    for _ in range(200):  # not going to get round once so ignoring destroy
        # find list of next satellite candidates
        larger = {pos: data[0] for pos, data in asteroids.items() if data[0] > laser_angle}
        if not larger:
            # circle +180 to -180
            laser_angle = -180.0
            larger = {pos: data[0] for pos, data in asteroids.items() if data[0] > laser_angle}
        # find next satellite
        minival = min(larger.values())
        laser_angle = minival
    # Find all asteroids with next angle
    miniasts = {(pos, data): data[1] for pos, data in asteroids.items() if data[0] == minival}
    miniast = min(miniasts, key=miniasts.get)
    return miniast[0][0]*100 + miniast[0][1]

if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}\n")
    print(f"\n    Part 2\n    {part2()}\n")
