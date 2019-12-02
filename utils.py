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


class IntcodeComputer():
    def __init__(self, program, noun, verb):
        self.program = program
        self.program[1] = noun
        self.program[2] = verb

    def execute(self):
        pc = 0
        while True:
            try:
                opcode = self.program[pc]
                a = self.program[pc+1]
                b = self.program[pc+2]
                c = self.program[pc+3]
            except IndexError:
                pass
            if opcode == 1:  # *c = *a+*b
                self.program[c] = self.program[a] + self.program[b]
            elif opcode == 2:  # *c = *a.*b
                self.program[c] = self.program[a] * self.program[b]
            elif opcode == 99:
                break
            else:
                assert False, f"Error PC={pc}\nPROGRAM={self.program}"
            if opcode in (1, 2):
                pc += 4
