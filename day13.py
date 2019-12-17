# pylint: disable=C0114, C0116, C0103, R0914
from utils import get_input, IntcodeComputer

DATA = get_input(13)

PROGRAM = list(map(int, DATA[0].split(',')))

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

CHARS = {
    EMPTY: ' ',
    WALL: '#',
    BLOCK: '~',
    PADDLE: '-',
    BALL: 'O'}

show = lambda display: [print("".join(line)) for line in display]


def get_display():
    # get dimensions from coords
    lenx = 42
    leny = 24

    # Create a blank surface of correct size
    arr = []
    for _ in range(leny):
        arr.append([CHARS[EMPTY]] * lenx)
    return arr


def part1():
    display = get_display()
    computer = IntcodeComputer(PROGRAM, input_fifo=[], signals=True)
    acc = 0
    while True:
        x = computer.execute()
        y = computer.execute()
        c = computer.execute()
        if computer.done:
            break
        display[y][x] = CHARS[c]
        if c == BLOCK:
            acc += 1
    # show(display)
    return acc


class Joystick:
    """An object which always returns the joystick direction when `pop`ped."""
    def __init__(self):
        self.val = 0

    def pop(self):
        return self.val

    def adjust(self, ballx, paddlex):
        if ballx < paddlex:
            self.val = -1
        elif ballx > paddlex:
            self.val = 1
        else:
            self.val = 0


def part2():
    """."""
    display = get_display()
    computer = IntcodeComputer(PROGRAM, signals=True)
    joystick = Joystick()
    computer.input_data = joystick
    computer.program[0] = 2  # add quarters
    score = paddle = ball = 0
    while True:
        x = computer.execute()
        y = computer.execute()
        c = computer.execute()
        if computer.done:
            break
        if x == -1 and y == 0:
            score = c
            # show(display)
        else:
            if c == BALL:
                ball = x
                joystick.adjust(ball, paddle)
            if c == PADDLE:
                paddle = x
                joystick.adjust(ball, paddle)
            display[y][x] = CHARS[c]
    return score


if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}\n")
    print(f"\n    Part 2\n    {part2()}\n")
