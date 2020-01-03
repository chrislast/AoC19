# pylint: disable=C0114, C0116, C0103, R0914
from utils import get_input, IntcodeComputer, bfs

DATA = get_input(15)

PROGRAM = list(map(int, DATA[0].split(',')))
NORTH, SOUTH, WEST, EAST = (1, 2, 3, 4)
WALL, OPEN, DONE = (0, 1, 2)

DROIDS = {}
STATS = dict(minx=0, miny=0, maxx=0, maxy=0, oxy=None)
DXDY = {NORTH:(1,0), SOUTH:(-1,0), EAST:(0,1), WEST:(0,-1)}

def show_map(textmap=None):
    if textmap is None:
        textmap = [list("#"*(STATS["maxx"]-STATS["minx"]+1)) for _ in range(STATS["maxy"]-STATS["miny"]+1)]
    for droid in DROIDS.values():
        textmap[droid.y-STATS["miny"]][droid.x-STATS["minx"]] = droid.char
    textmap[-STATS["miny"]][-STATS["minx"]] = "@"
    # print('\n'.join([''.join(_) for _ in textmap]))
    return textmap

# Creates a droid army, would be better to clone or reuse original
# than replay entire route each time though
class Droid():
    def __init__(self, route):
        self.cpu = IntcodeComputer(PROGRAM, input_fifo=route, signals=True)
        self.x = 0
        self.y = 0
        self.char = '#'
        self.neighbours = []
        self.state = OPEN
        for move in route:
            self.state = self.cpu.execute()
            self.x += DXDY[move][1]
            self.y += DXDY[move][0]
        self.cpu = len(route)
        DROIDS[(self.x, self.y)] = self
        if self.x < STATS["minx"]:
            STATS["minx"] = self.x
        if self.x > STATS["maxx"]:
            STATS["maxx"] = self.x
        if self.y < STATS["miny"]:
            STATS["miny"] = self.y
        if self.y > STATS["maxy"]:
            STATS["maxy"] = self.y
        if self.state == OPEN:
            self.char = ' '
            # Add surrounding map nodes if not visited already
            if (self.x, self.y+1) not in DROIDS:
                Droid(route + (NORTH,))
            if (self.x, self.y-1) not in DROIDS:
                Droid(route + (SOUTH,))
            if (self.x+1, self.y) not in DROIDS:
                Droid(route + (EAST,))
            if (self.x-1, self.y) not in DROIDS:
                Droid(route + (WEST,))
        elif self.state == DONE:
            self.char = 'o'
            STATS["oxy"] = (self.x, self.y)


def part1():
    droid = Droid(()) # create the first droid
    textmap = show_map()
    route = bfs(textmap)
    for x, y in route:
        if textmap[y][x] == ' ':
            textmap[y][x] = '.'
    if __name__ == "__main__":
        for _ in textmap:
            print(''.join(_))
    return len(route)-1


def part2():
    """."""
    textmap = show_map()
    route = bfs(textmap, start="o", end=None)
    return len(route)-1


if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}\n")
    print(f"\n    Part 2\n    {part2()}\n")
