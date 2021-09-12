from utils import *
from collections import deque
import numpy

DAY = day(__file__)
DATA = get_input(DAY)

xDATA="""
#########
#b.A.@.a#
#########
""".strip().split()

xDATA="""
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
""".strip().split()

@part1
def part1(expect=5808):
    return 0
    bfs = deque()
    MAP = numpy.array(list(map(list, DATA)))
    y, x = map(int, numpy.where(MAP == "@"))
    MAP[y,x] = "."
    # add the start position
    bfs.append((MAP, set(), x, y, 0, set()))
    dx, dy = MAP.shape
    size = dx * dy
    c = 0
    found = set()
    while True:
        m, s, x, y, c, o = bfs.popleft()
        if "a" <= m[y,x] <= "z": # key found
            # so update map and clear "seen" set
            door = m[y,x].upper()
            m = m.copy()
            m[y,x] = "."  # Remove key from new map
            # find the door we "opened"
            try:
                new_found = door + ''.join(sorted(o))
                o.add(door)
                if new_found in found:
                    # we already found a quicker way to this position
                    # with these keys so close this path
                    continue
                found.add(new_found)
                print(c, len(bfs), "opened", new_found)
                if len(new_found) == 26:
                    break
                yd, xd = map(int, numpy.where(MAP == door))
            except:
                # if there is no door we're done!
                break
            m[yd,xd] = "." # Remove door from new map
            # reset seen set so we can reuse map
            s = set()
        s.add((y,x))
        for dx,dy in ((1,0),(0,1),(-1,0),(0,-1)):
            newx = x+dx
            newy = y+dy
            char = m[y+dy,x+dx]
            if (newy, newx) not in s:
                if char == "." or "a" <= char <= "z":
                    bfs.append((m, s, newx, newy, c+1, o.copy()))
    return c

@part2
def part2(expect=130933530):
    bfs = deque()
    MAP = numpy.array(list(map(list, DATA)))
    y, x = map(int, numpy.where(MAP == "@"))
    import pdb; pdb.set_trace()
    MAP[y-1:y+2,x-1:x+2] = numpy.array(list(map(list, [".#.","###",".#."])))
    # add the start positions
    robos = dict()
    robos[1] = dict(x=x-1, y=y-1, steps=0)
    robos[2] = dict(x=x+1, y=y-1, steps=0)
    robos[3] = dict(x=x-1, y=y+1, steps=0)
    robos[4] = dict(x=x+1, y=y+1, steps=0)
    bfs.append((MAP, set(), robos, set()))


    # todo
    pick a robot
    find a door
    switch to robot
    find key


    dx, dy = MAP.shape
    size = dx * dy
    c = 0
    found = set()
    while True:
        m, s, x, y, c, o = bfs.popleft()
        if "a" <= m[y,x] <= "z": # key found
            # so update map and clear "seen" set
            door = m[y,x].upper()
            m = m.copy()
            m[y,x] = "."  # Remove key from new map
            # find the door we "opened"
            try:
                new_found = door + ''.join(sorted(o))
                o.add(door)
                if new_found in found:
                    # we already found a quicker way to this position
                    # with these keys so close this path
                    continue
                found.add(new_found)
                print(c, len(bfs), "opened", new_found)
                if len(new_found) == 26:
                    break
                yd, xd = map(int, numpy.where(MAP == door))
            except:
                # if there is no door we're done!
                break
            m[yd,xd] = "." # Remove door from new map
            # reset seen set so we can reuse map
            s = set()
        s.add((y,x))
        for dx,dy in ((1,0),(0,1),(-1,0),(0,-1)):
            newx = x+dx
            newy = y+dy
            char = m[y+dy,x+dx]
            if (newy, newx) not in s:
                if char == "." or "a" <= char <= "z":
                    bfs.append((m, s, newx, newy, c+1, o.copy()))
    return c

