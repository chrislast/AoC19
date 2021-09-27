# pylint: disable=C0114, C0116, C0103, R0914
from utils import get_input, TRACE, Map
from copy import deepcopy

DATA = get_input(24)

def hash(img):
    # turn e.g. 5x5 image into string
    # '#.##.###.##...###..#.#...'
    s = img.img.tobytes().decode()
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
    img = Map(DATA)
    while True:
        h = hash(img)
        if h in seen:
            break
        seen.add(h)
        img = turn(img)
    #img.show()
    img.save("images/day24p1.png")
    return h


def part2():
    pass


if __name__ == "__main__":
    # 580 steps
    print(f"\n    Part 1\n    {part1()}\n")
    # wow - 6362 steps across 127 layers!
    print(f"\n    Part 2\n    {part2()}\n")
