# pylint: disable=C0114, C0116, C0103, R0914
from utils import get_input, TRACE, Map
from copy import deepcopy

DATA = get_input(24)

class BugMap(Map):
    def count_bugs(self):
        w,h = self.img.size
        return sum([int(self.get((x,y))==ord("#")) for x in range(w) for y in range(h)])

    def hash(self):
        # turn e.g. 5x5 image into string
        # '#.##.###.##...###..#.#...'
        s = self.img.tobytes().decode()
        s = s[::-1] # reverse string
        # turn map to a binary string
        s = s.replace(".","0")
        s = s.replace("#","1")
        # return converted binary as int
        return int(s,2)

def turn(img):
    img2 = deepcopy(img)
    xx,yy = img2.img.size
    for x in range(xx):
        for y in range(yy):
            adjacent = 0
            if x+1 < xx and img.get((x+1,y)) == ord("#"):
                adjacent += 1
            if y+1 < yy and img.get((x,y+1)) == ord("#"):
                adjacent += 1
            if x-1 >= 0 and img.get((x-1,y)) == ord("#"):
                adjacent += 1
            if y-1 >= 0 and img.get((x,y-1)) == ord("#"):
                adjacent += 1
            if img.get((x,y)) == ord("#"):
                if adjacent != 1:
                    # kill bug
                    img2.set((x,y),".")
            else:
                if adjacent in (1,2):
                    img2.set((x,y),"#")
    return img2

def part1():
    # initialise the image map
    seen = set()
    img = BugMap(DATA)
    while True:
        h = img.hash()
        if h in seen:
            break
        seen.add(h)
        img = turn(img)
    #img.show()
    img.save("images/day24p1.png")
    return h


EMPTY = BugMap(("."*5,)*5)

# outer layer right, left, up, down neighbours
OUTR = (-1,3,2)
OUTL = (-1,1,2)
OUTU = (-1,2,1)
OUTD = (-1,2,3)

# inner layer right, left, up, down neighbours
INR = ((1,0,0),(1,0,1),(1,0,2),(1,0,3),(1,0,4))
INL = ((1,4,0),(1,4,1),(1,4,2),(1,4,3),(1,4,4))
INU = ((1,0,4),(1,1,4),(1,2,4),(1,3,4),(1,4,4))
IND = ((1,0,0),(1,1,0),(1,2,0),(1,3,0),(1,4,0))

# Adjacent tiles for each x,y as offsets
NEIGH = { # +x      +y      -x      -y
  (0,0): [(0,1,0),(0,0,1), OUTL  , OUTU  ],
  (1,0): [(0,2,0),(0,1,1),(0,0,0), OUTU  ],
  (2,0): [(0,3,0),(0,2,1),(0,1,0), OUTU  ],
  (3,0): [(0,4,0),(0,3,1),(0,2,0), OUTU  ],
  (4,0): [ OUTR  ,(0,4,1),(0,3,0), OUTU  ],
  (0,1): [(0,1,1),(0,0,2), OUTL  ,(0,0,0)],
  (1,1): [(0,2,1),(0,1,2),(0,0,1),(0,1,0)],
  (2,1): [(0,3,1), *IND  ,(0,1,1),(0,2,0)],
  (3,1): [(0,4,1),(0,3,2),(0,2,1),(0,3,0)],
  (4,1): [ OUTR  ,(0,4,2),(0,3,1),(0,4,0)],
  (0,2): [(0,1,2),(0,0,3), OUTL  ,(0,0,1)],
  (1,2): [ *INR  ,(0,1,3),(0,0,2),(0,1,1)],
  (2,2): [],
  (3,2): [(0,4,2),(0,3,3), *INL  ,(0,3,1)],
  (4,2): [ OUTR  ,(0,4,3),(0,3,2),(0,4,1)],
  (0,3): [(0,1,3),(0,0,4), OUTL  ,(0,0,2)],
  (1,3): [(0,2,3),(0,1,4),(0,0,3),(0,1,2)],
  (2,3): [(0,3,3),(0,2,4),(0,1,3), *INU  ],
  (3,3): [(0,4,3),(0,3,4),(0,2,3),(0,3,2)],
  (4,3): [ OUTR  ,(0,4,4),(0,3,3),(0,4,2)],
  (0,4): [(0,1,4), OUTD  , OUTL  ,(0,0,3)],
  (1,4): [(0,2,4), OUTD  ,(0,0,4),(0,1,3)],
  (2,4): [(0,3,4), OUTD  ,(0,1,4),(0,2,3)],
  (3,4): [(0,4,4), OUTD  ,(0,2,4),(0,3,3)],
  (4,4): [ OUTR  , OUTD  ,(0,3,4),(0,4,3)],
}

def grow(world):
    layers=deepcopy(world)
    layers[min(layers)-1] = deepcopy(EMPTY)
    layers[max(layers)+1] = deepcopy(EMPTY)
    for l in layers:
        for x in range(5):
            for y in range(5):
                acc = 0
                for ll,xx,yy in NEIGH[x,y]:
                    if l+ll in world:
                        acc += int(world[l+ll].get((xx,yy))==ord("#"))
                if layers[l].get((x,y)) == ord("#"):
                    if acc != 1:
                        # kill bug
                        layers[l].set((x,y),".")
                else:
                    if acc in (1,2):
                        layers[l].set((x,y),"#")
    # cleanup unused layers to reduce overheads
    while layers[min(layers)].count_bugs() == 0:
        layers.pop(min(layers))
    while layers[max(layers)].count_bugs() == 0:
        layers.pop(max(layers))
    return layers

def part2():
    # initialise the image map
    world = {0: BugMap(DATA)}
    for _ in range(200):
        world = grow(world)
    # for _ in range(0,25,5):
    #     for __ in range(min(world),max(world)):
    #         l1 = world[__].img.tobytes().decode()
    #         print(f"{l1[_+0:_+5]} ",end="")
    #     print("")
    return sum([_.count_bugs() for _ in world.values()])


if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}\n")
    print(f"\n    Part 2\n    {part2()}\n")
