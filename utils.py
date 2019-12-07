""" Advent of Code 2019 """
# pylint: disable=C0114, C0115, C0116, C0103
import re
from pathlib import Path

###########################


def get_input(day, converter=None):
    """."""
    input_file = Path('input') / (str(day) + ".txt")
    with open(input_file) as f:
        text = list(map(str.strip, f.readlines()))
    print(f'INPUT_TEXT={text}'[:75] + '...]')
    if converter:
        return list(map(converter, text))
    return text


def sscanf(text, regex):
    _ = re.compile(regex)
    return _.match(text).groups()


# operations
ADD = 1
MUL = 2
INPUT = 3
OUTPUT = 4
# Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
JIT = 5
# Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
JIF = 6
# Opcode 7 is less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
LT = 7
# Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
EQ = 8
EXIT = 99

# parameter modes
POSITION = 0
IMMEDIATE = 1


class IntcodeComputer():
    def __init__(self, program, noun=None, verb=None, input_fifo=None):
        self.program = program
        if noun is not None:
            self.program[1] = noun
        if verb is not None:
            self.program[2] = verb
        if input_fifo is not None:
            self.input_data = list(reversed(input_fifo))
        self.output_data = []

    def set(self, addr, val):
        self.program[self.program[addr]] = val

    def get(self, addr):
        return self.program[self.program[addr]]

    def execute(self):
        pc = 0

        while True:
            try:
                opcode = "%08d" % self.program[pc]
                inst = int(opcode[-2:])
                mode = [int(_) for _ in opcode[-3::-1]]
                p = []
                t = []

                for n in range(6):
                    if mode[n] == POSITION:
                        p.append(self.program[self.program[pc+1+n]])
                        t.append(f"*{self.program[pc+1+n]}({p[-1]})")
                    elif mode[n] == IMMEDIATE:
                        p.append(self.program[pc+1+n])
                        t.append(f"*{pc+1+n}({self.program[pc+1+n]})")
                    else:
                        if inst != 99:
                            assert False, f"Unknown address mode {mode[n]} in {opcode}"
            except IndexError:
                pass

            if inst == ADD:
                self.set(pc+3, p[0] + p[1])
                dbg = f"[{pc}] {opcode} ADD {t[0]}, {t[1]}, {t[2]}"
                pc += 4

            elif inst == MUL:
                self.set(pc+3, p[0] * p[1])
                dbg = f"[{pc}] {opcode} MUL {t[0]}, {t[1]}, {t[2]}"
                pc += 4

            elif inst == INPUT:
                self.set(pc+1, self.input_data.pop())
                dbg = f"[{pc}] {opcode} INPUT {t[0]}"
                pc += 2

            elif inst == OUTPUT:
                self.output_data.append(p[0])
                dbg = f"[{pc}] {opcode} OUTPUT {t[0]}"
                pc += 2

            # Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets the instruction
            # pointer to the value from the second parameter. Otherwise, it does nothing.
            elif inst == JIT:
                dbg = f"[{pc}] {opcode} JIT {t[0]}, {t[1]}"
                if p[0]:
                    pc = p[1]
                else:
                    pc += 3

            # Opcode 6 is jump-if-false: if the first parameter is zero, it sets the instruction
            # pointer to the value from the second parameter. Otherwise, it does nothing.
            elif inst == JIF:
                dbg = f"[{pc}] {opcode} JIF {t[0]}, {t[1]}"
                if not p[0]:
                    pc = p[1]
                else:
                    pc += 3

            # Opcode 7 is less than: if the first parameter is less than the second parameter, it
            # stores 1 in the position given by the third parameter. Otherwise, it stores 0.
            elif inst == LT:
                dbg = f"[{pc}] {opcode} LT {t[0]}, {t[1]}, {t[2]}"
                if p[0] < p[1]:
                    self.set(pc+3, 1)
                else:
                    self.set(pc+3, 0)
                pc += 4

            # Opcode 8 is equals: if the first parameter is equal to the second parameter, it stores
            # 1 in the position given by the third parameter. Otherwise, it stores 0.
            elif inst == EQ:
                dbg = f"[{pc}] {opcode} EQ {t[0]}, {t[1]}, {t[2]}"
                if p[0] == p[1]:
                    self.set(pc+3, 1)
                else:
                    self.set(pc+3, 0)
                pc += 4

            # exit
            elif inst == EXIT:
                # print(f"[{pc}] {opcode} EXIT")
                break

            # error
            else:
                assert False, f"Error PC={pc} ({opcode})\nINST={inst}\nPARAM={p}\nPROGRAM={self.program}"

            # print(dbg)

        return self.output_data
