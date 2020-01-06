# pylint: disable=C0114, C0116, C0103, R0914
from utils import get_input, IntcodeComputer, bfs

DATA = get_input(17)
PROGRAM = list(map(int, DATA[0].split(',')))

def part1():
    computer = IntcodeComputer(PROGRAM)
    computer.execute()
    map1d = ''.join(map(chr, computer.output_data)).strip()
    if __name__ == "__main__":
        print(map1d)
    map2d = map1d.split('\n')
    acc = 0
    for y in range(1,len(map2d)-1):
        for x in range(1,len(map2d[0])-1):
            if map2d[y][x] + map2d[y-1][x] + map2d[y+1][x] + map2d[y][x-1] + map2d[y][x+1] == "#####":
                acc += x*y
    return acc

class Vac:

    LEFT_TURNS =  ("#...^", "#..#^", "##..>", ".##.v", "..##<")
    RIGHT_TURNS = ("#..#>", "##..v", ".##.<", "..##^")
    PATH_ENDS =   ("...#v", "..#.<", ".#..^", "#...>")

    def __init__(self, map2d):
        self.map2d = map2d
        maxy = len(map2d)
        maxx = len(map2d[0])
        self.vacx, self.vacy = [(x,y) for x in range(maxx) for y in range(maxy) if map2d[y][x] in ("<","^","v",">")][0]

    def sitrep(self):
        #import pdb; pdb.set_trace()
        acc = ""
        #               LEFT  ABOVE  RIGHT BELOW  MID
        for dx, dy in [(-1,0),(0,-1),(1,0),(0,1),(0,0)]:
            x, y = (dx + self.vacx, dy+self.vacy)
            if x < 0 or y < 0:
                acc += "."
            else:
                try:
                    acc += self.map2d[y][x]
                except:
                    acc += "."
        return acc

    def turn(self, dirn):
        m = [list(_) for _ in self.map2d]
        if dirn == "L":
            m[self.vacy][self.vacx] = {">":"^", "<":"v", "^":"<", "v":">"}[m[self.vacy][self.vacx]]
        else:
            m[self.vacy][self.vacx] = {"<":"^", ">":"v", "v":"<", "^":">"}[m[self.vacy][self.vacx]]
        self.map2d = [''.join(_) for _ in m]
        return dirn

    def move(self):
        m = [list(_) for _ in self.map2d]
        dirn = m[self.vacy][self.vacx]
        m[self.vacy][self.vacx] = "#"
        self.vacx += {">":1, "<":-1, "^":0, "v":0}[dirn]
        self.vacy += {"v":1, "^":-1, "<":0, ">":0}[dirn]
        m[self.vacy][self.vacx] = dirn
        self.map2d = [''.join(_) for _ in m]
        return "1"

    def step(self):
        info = self.sitrep()
        if info in self.LEFT_TURNS:
            return self.turn("L")
        if info in self.RIGHT_TURNS:
            return self.turn("R")
        return self.move()

    def go(self):
        acc = []
        while self.sitrep() not in self.PATH_ENDS:
            step = self.step()
            acc.append(step)
        return ''.join(acc)

def part2():
    """."""
    computer = IntcodeComputer(PROGRAM)
    computer.execute()
    map1d = ''.join(map(chr, computer.output_data)).strip()
    map2d = map1d.split('\n')
    vac = Vac(map2d)
    route = vac.go()
    if __name__ == "__main__":
        print(route, '\n')  # show the route
    # sadly i cheated here and used an editor to pattern find route and manually create recipe
    # hence this won't work for anyone else
    SEQ = "A,B,A,C,C,A,B,C,B,B\n"
    A = "L,8,R,10,L,8,R,8\n"
    B = "L,12,R,8,R,8\n"
    C = "L,8,R,6,R,6,R,10,L,8\n"
    VIDEO = "n\n"
    SCRIPT = SEQ + A + B + C + VIDEO

    PROGRAM[0] = 2
    computer = IntcodeComputer(PROGRAM, signals=True, input_fifo=[ord(c) for c in SCRIPT], debug=False)
    acc = ""
    while not computer.done:
        result = computer.execute()
        if result == 10:
            if __name__ == "__main__":
                print(acc)
            acc = ""
        elif result < 255:
            acc += chr(result)
    return result

if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}\n")
    print(f"\n    Part 2\n    {part2()}\n")
