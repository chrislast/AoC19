# pylint: disable=C0114, C0116, C0103, R0914
from utils import get_input, IntcodeComputer, bfs, TRACE
import re
from PIL import Image
from collections import deque

DATA = get_input(20, strip=False)
PALETTE = [0]*768
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def update_palette(c, r, g, b):
    """map char to rgb in pallette"""
    n=ord(c)*3
    PALETTE[n] = r
    PALETTE[n+1] = g
    PALETTE[n+2] = b

update_palette(".",0,255,0) # green paths
update_palette("#",255,0,0) # red walls
update_palette("*",255,255,0) # yellow visited
for c in ALPHA:
    update_palette(c,0,0,255) # blue teleporters

WIDTH = 117
HEIGHT = 119

def load_map():
    # use a color palette image to store array
    img = Image.new('P', (WIDTH,HEIGHT))
    img.putpalette(PALETTE)
    # populate map
    for y in range(HEIGHT):
        for x in range(WIDTH):
            try:
                if DATA[y][x] != " ":
                    img.putpixel((x,y),ord(DATA[y][x]))
            except:
                break
    return img

DOT = ord(".")
WALL = ord("#")
VISITED = ord("*")

def get_teleport_map(img):
    tmap=dict()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if p:=img.getpixel((x,y)):
                if chr(p) in ALPHA:
                    try:
                        if img.getpixel((x+1,y)) == DOT: # dot after
                            pos = (x+1,y)
                            label = chr(img.getpixel((x-1,y)))+chr(p)
                        elif img.getpixel((x-1,y)) == DOT: # dot before
                            pos = (x-1,y)
                            label = chr(p)+chr(img.getpixel((x+1,y)))
                        elif img.getpixel((x,y-1)) == DOT: # dot above
                            pos = (x,y-1)
                            label = chr(p)+chr(img.getpixel((x,y+1)))
                        elif img.getpixel((x,y+1)) == DOT: # dot below
                            pos = (x,y+1)
                            label = chr(img.getpixel((x,y-1)))+chr(p)
                        else:
                            continue
                        if label not in tmap:
                            tmap[label] = pos
                        else:
                            p1 = tmap[label]
                            tmap[pos] = p1
                            tmap[p1] = pos
                            tmap.pop(label) # the label is no longer needed
                            # print(f"linked {label} {p1}<->{pos}")
                    except:
                        pass
    return tmap

def bfs_img_with_tmap(img, tmap):
    """
    Breadth-first search image with teleports
    """
    # find the shortest route from start to end
    visited = set()
    start = tmap["AA"]
    end = tmap["ZZ"]
    queue = deque()
    queue.append((0,*start))

    while True:
        # add the step to visited list
        n, x, y = queue.popleft()
        img.putpixel((x,y), VISITED)
        visited.add((x,y))

        # If end reached return steps to end
        if (x,y) == end:
            return n

        # Add new routes to queue
        for xx in x+1, x-1:
            if (xx,y) not in visited:
                if img.getpixel((xx,y)) == DOT:
                    queue.append((n+1,xx,y))
        for yy in y+1, y-1:
            if (x,yy) not in visited:
                if img.getpixel((x,yy)) == DOT:
                    queue.append((n+1,x,yy))
        if (x,y) in tmap:
            queue.append((n+1,*tmap[(x,y)]))

        # If search queue is empty report unfound (-1)
        if not queue:
            return -1

DIGITS = [
    [" ### ","#   #","#  ##","# # #","##  #"," ### ","     ",],
    ["  #  "," ##  ","  #  ","  #  ","  #  "," ### ","     ",],
    [" ### ","#   #","   # ","  #  "," #   ","#####","     ",],
    ["#####","   # ","  #  ","   # ","#   #"," ### ","     ",],
    ["   # ","  ## "," # # ","#####","   # ","   # ","     ",],
    ["#####","#    ","#### ","    #","#   #"," ### ","     ",],
    [" ### ","#    ","#### ","#   #","#   #"," ### ","     ",],
    ["#####","    #","   # ","  #  ","  #  ","  #  ","     ",],
    [" ### ","#   #"," ### ","#   #","#   #"," ### ","     ",],
    [" ### ","#   #","#   #"," ####","    #"," ### ","     ",],
]

def label(img, layer):
    """only required for visualisation"""
    a = DIGITS[layer // 100 % 10]
    b = DIGITS[layer // 10 % 10]
    c = DIGITS[layer % 10]
    for y, row in enumerate(a):
        for x, char in enumerate(row):
            if char=="#":
                img.putpixel((x+50,y+50), VISITED)
    for y, row in enumerate(b):
        for x, char in enumerate(row):
            if char=="#":
                img.putpixel((x+56,y+50), VISITED)
    for y, row in enumerate(c):
        for x, char in enumerate(row):
            if char=="#":
                img.putpixel((x+62,y+50), VISITED)

def bfs_img_with_tmap_3d(img, tmap):
    """
    Breadth-first search image with teleports multi-dimensional
    """
    # find the shortest route from start to end
    depth = 0 # start at layer 0
    start = tmap["AA"]
    end = tmap["ZZ"]
    queue = deque()
    queue.append((0, depth, *start))
    imgs=[img.copy()]
    visited = [set()]
    outer = lambda x,y: x==2 or x==114 or y==2 or y==116

    # close outer portals in layer 0
    for portal in tmap:
        if isinstance(portal, tuple):
            if outer(*portal):
                visited[0].add(portal)
                imgs[0].putpixel(portal, WALL)
    label(imgs[0],0)

    def add_layer():
        """create a new lower layer with no exits"""
        visited.append(set())
        imgs.append(img.copy())
        # wall off lower layer exits
        imgs[-1].putpixel(tmap["AA"], WALL)
        imgs[-1].putpixel(tmap["ZZ"], WALL)
        label(imgs[-1], d) # just for fun

    while True:
        # add the step to visited list
        # num, depth, xpos, ypos
        n, d, x, y = queue.popleft()
        imgs[d].putpixel((x,y), VISITED)
        visited[d].add((x,y))

        # If end reached return steps to end
        if (x,y) == end:
            imgs[0].save("images/day20p2.gif", append_images=imgs[1:], save_all=True, duration=100, loop=1, palette=PALETTE)
            return n

        # Add new routes to queue
        for xx in x+1, x-1:
            if (xx,y) not in visited[d]:
                if imgs[d].getpixel((xx,y)) == DOT:
                    queue.append((n+1,d,xx,y))
        for yy in y+1, y-1:
            if (x,yy) not in visited[d]:
                if imgs[d].getpixel((x,yy)) == DOT:
                    queue.append((n+1,d,x,yy))
        if (x,y) in tmap:
            # optimisation! don't descend deeper than max portals
            if d > len(tmap):
                continue
            if outer(x,y):
                if tmap[(x,y)] not in visited[d-1]:
                    queue.append((n+1,d-1,*tmap[(x,y)]))
            else:
                try:
                    if tmap[(x,y)] not in visited[d+1]:
                        queue.append((n+1,d+1,*tmap[(x,y)]))
                except IndexError:
                    add_layer()
                    queue.append((n+1,d+1,*tmap[(x,y)]))

        # If search queue is empty report unfound (-1)
        if not queue:
            return -1

def part1():
    # initialise the image map
    img = load_map()
    # find teleporters
    tmap = get_teleport_map(img)
    # breadth first search AA to ZZ with teleports!
    steps = bfs_img_with_tmap(img,tmap)
    #img.show()
    img.save("images/day20p1.png")
    return steps

def part2():
    # initialise the image map
    img = load_map()
    # find teleporters
    tmap = get_teleport_map(img)
    # breadth first search AA to ZZ with teleports!
    steps = bfs_img_with_tmap_3d(img,tmap)
    return steps


if __name__ == "__main__":
    # 580 steps
    print(f"\n    Part 1\n    {part1()}\n")
    # wow - 6362 steps across 127 layers!
    print(f"\n    Part 2\n    {part2()}\n")
