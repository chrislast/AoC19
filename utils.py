""" Advent of Code 2019 """
# pylint: disable=C0114, C0115, C0116, C0103
import re
import math
from pathlib import Path

###########################


def get_input(day, converter=None, debug=False):
    """."""
    input_file = Path('input') / (str(day) + ".txt")
    with open(input_file) as f:
        text = list(map(str.strip, f.readlines()))
    if debug:
        print(f'INPUT_TEXT={text}'[:75] + '...]')
    if converter:
        return list(map(converter, text))
    return text


def lcm(*args):
    """find lowest common multiple of all integer arguments
    lcm(15,20,12) ==> 60
    """
    _lcm = int(args[0])
    for i in args[1:]:
        _lcm = int(_lcm*i/math.gcd(_lcm, int(i)))
    return _lcm


def sscanf(text, regex, converters=()):
    r"""
    example:
    sscanf("<x=-7, y=17, z=-11>",
           "x=(-?\d+), y=(-?\d+), z=(-?\d+)",
           [int]*3)
    ==> [-7, 17, -11]
    """
    _ = re.compile(regex)
    res = list(_.search(text).groups())
    for idx, cnv in enumerate(converters):
        res[idx] = cnv(res[idx])
    return tuple(res)


def bfs(textmap, start="@", end="o", wall="#", open=" "):
    """
    Breadth-first search a text map
    e.g.
    textmap = [list('#'*5), ['#','@','','o','#'], list('#'*5)]
    #####
    #@ o#
    #####
    """
    # create the search space graph
    graph = {}
    startpos = None
    endpos = None
    for y in range(len(textmap)):
        for x in range(len(textmap[0])):
            if textmap[y][x] != wall:
                graph[(x, y)] = []
                for dx, dy in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                    if textmap[dy][dx] != wall:
                        graph[(x, y)].append((dx, dy))
                if textmap[y][x] == start:
                    startpos = (x, y)

    # find the shortest route from start to end
    visited = set()
    queue = [[startpos]]
    idx = 0

    while True:
        # add the route destination to visited list
        x, y = queue[idx][-1]
        visited.add((x,y))

        # If end reached return route to end
        if textmap[y][x] == end:
            return queue[idx]

        # Add new route to queue if "edge" not already visited
        for pos in graph[(x,y)]:
            if pos not in visited:
                queue.append(queue[idx]+[pos])
        idx += 1

        # If all nodes filled return final node route
        if idx == len(queue):
            return queue[-1]


# operations
ADD = 1
MUL = 2
INPUT = 3
OUTPUT = 4
JIT = 5
JIF = 6
LT = 7
EQ = 8
RBO = 9
EXIT = 99

# parameter modes
POSITION = 0
IMMEDIATE = 1
RELATIVE = 2


class IntcodeComputer():
    def __init__(self, program=None, noun=None, verb=None, input_fifo=None, signals=False,
                 debug=False):
        if program:
            self.load(program[:])
        if noun is not None:
            self.program[1] = noun
        if verb is not None:
            self.program[2] = verb
        if input_fifo is not None:
            self.input_data = list(reversed(input_fifo))
        else:
            self.input_data = list()
        self.output_data = list()
        self.signal = signals
        self.show_debug = debug
        self.pc = 0
        self.relative_pc = 0
        self.done = False

    def debug(self, txt):
        if self.show_debug:
            print(txt)

    def add_input(self, val):
        self.input_data.insert(0, val)

    def get_output(self):
        return self.output_data[-1]

    def load(self, program):
        self.program = program + [0] * 100000
        self.pc = 0

    def set(self, addr, val, mode):
        if mode == RELATIVE:
            self.program[self.program[addr]+self.relative_pc] = val
        elif mode == POSITION:
            self.program[self.program[addr]] = val
        elif mode == IMMEDIATE:
            self.program[addr] = val
        else:
            assert False, "Unknown mode"

    def get(self, addr, mode):
        if mode == RELATIVE:
            return self.program[self.program[addr]+self.relative_pc]
        if mode == POSITION:
            return self.program[self.program[addr]]
        if mode == IMMEDIATE:
            return self.program[addr]
        assert False, "Unknown mode"
        return None

    def execute(self):  # pylint: disable=R0912, R0915
        while True:
            try:
                opcode = "%08d" % self.program[self.pc]
                inst = int(opcode[-2:])
                mode = [int(_) for _ in opcode[-3::-1]]
                p = []
                t = []

                for n in range(6):
                    if mode[n] == POSITION:
                        p.append(self.program[self.program[self.pc+1+n]])
                        t.append(f"*{self.program[self.pc+1+n]}({p[-1]})")
                    elif mode[n] == IMMEDIATE:
                        p.append(self.program[self.pc+1+n])
                        t.append(f"*{self.pc+1+n}({self.program[self.pc+1+n]})")
                    elif mode[n] == RELATIVE:
                        p.append(self.program[self.program[self.pc+1+n]+self.relative_pc])
                        t.append(f"*{self.program[self.pc+1+n]}[{self.relative_pc}]({p[-1]})")
                    else:
                        if inst != 99:
                            assert False, f"Unknown address mode {mode[n]} in {opcode}"
            except IndexError:
                pass

            if inst == ADD:
                val = p[0] + p[1]
                self.set(self.pc+3, val, mode[2])
                self.debug(f"[{self.pc}] {opcode} ADD {t[0]}, {t[1]}, {t[2]}")
                self.pc += 4

            elif inst == MUL:
                val = p[0] * p[1]
                self.set(self.pc+3, val, mode[2])
                self.debug(f"[{self.pc}] {opcode} MUL {t[0]}, {t[1]}, {t[2]}")
                self.pc += 4

            elif inst == INPUT:
                val = self.input_data.pop()
                self.set(self.pc+1, val, mode[0])
                self.debug(f"[{self.pc}] {opcode} INPUT {t[0]} <- {val}")
                self.pc += 2

            elif inst == OUTPUT:
                self.output_data.append(p[0])
                self.debug(f"[{self.pc}] {opcode} OUTPUT {t[0]} -> {self.output_data[-1]}")
                self.pc += 2
                if self.signal:
                    return p[0]

            # Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction
            # pointer to the value from the second parameter. Otherwise, it does nothing.
            elif inst == JIT:
                self.debug(f"[{self.pc}] {opcode} JIT {t[0]}, {t[1]}")
                if p[0]:
                    self.pc = p[1]
                else:
                    self.pc += 3

            # Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction
            # pointer to the value from the second parameter. Otherwise, it does nothing.
            elif inst == JIF:
                self.debug(f"[{self.pc}] {opcode} JIF {t[0]}, {t[1]}")
                if not p[0]:
                    self.pc = p[1]
                else:
                    self.pc += 3

            # Opcode 7 is less than: if the first parameter is less than the second parameter, it
            # stores 1 in the position given by the third parameter. Otherwise, it stores 0.
            elif inst == LT:
                self.debug(f"[{self.pc}] {opcode} LT {t[0]}, {t[1]}, {t[2]}")
                val = int(p[0] < p[1])
                self.set(self.pc+3, val, mode[2])
                self.pc += 4

            # Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores
            # 1 in the position given by the third parameter. Otherwise, it stores 0.
            elif inst == EQ:
                self.debug(f"[{self.pc}] {opcode} EQ {t[0]}, {t[1]}, {t[2]}")
                val = int(p[0] == p[1])
                self.set(self.pc+3, val, mode[2])
                self.pc += 4

            # Opcode 9 adjusts the relative base by the value of its only parameter. The relative
            # base increases (or decreases, if the value is negative) by the value of the parameter.
            elif inst == RBO:
                self.relative_pc += p[0]
                self.debug(f"[{self.pc}] {opcode} RBO {t[0]} -> {self.relative_pc}")
                self.pc += 2

            # exit
            elif inst == EXIT:
                self.done = True
                if self.output_data:
                    self.debug(f"[{self.pc}] {opcode} EXIT ({self.output_data[-1]})")
                    return self.output_data[-1]
                self.debug(f"[{self.pc}] {opcode} EXIT")
                return None

            # error
            else:
                assert False, f"Error PC={self.pc} ({opcode})"

        return None
