# pylint: disable=C0114, C0116, C0103, R0914
from utils import get_input, IntcodeComputer

DATA = get_input(11)

PROGRAM = list(map(int, DATA[0].split(',')))

BLACK = 0
WHITE = 1

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

TURN = {LEFT: {LEFT: DOWN, DOWN: RIGHT, RIGHT: UP, UP: LEFT},
        RIGHT: {LEFT: UP, UP: RIGHT, RIGHT: DOWN, DOWN: LEFT}}

COLOUR = {BLACK: " ", WHITE: "#"}


class Popper:
    """An object which always returns the same value when `pop`ped."""
    def __init__(self, val):
        self.val = val

    def pop(self):
        return self.val


def move(x, y, direction):
    if direction == UP:
        return x, y+1
    if direction == DOWN:
        return x, y-1
    if direction == LEFT:
        return x-1, y
    if direction == RIGHT:
        return x+1, y
    assert False, direction
    return None


def get_coords(computer, coords):
    x = y = 0
    direction = UP
    while not computer.done:
        # if never visited it's black
        old_colour = coords.get((x, y), BLACK)
        # give existing colour to all input commands
        computer.input_data = Popper(old_colour)
        # get new colour
        new_colour = computer.execute()
        coords[(x, y)] = new_colour
        # get new direction
        turn = computer.execute()
        direction = TURN[turn][direction]
        # get new position after move
        x, y = move(x, y, direction)
    return coords


def get_map(coords):
    # get dimensions from coords
    xs = list([x for x, y in coords])
    ys = list([y for x, y in coords])
    minx = min(xs)
    maxx = max(xs)
    lenx = maxx - minx + 1
    miny = min(ys)
    maxy = max(ys)
    leny = maxy - miny + 1

    # Create a blank surface of correct size
    arr = []
    for _ in range(leny):
        arr.append([COLOUR[BLACK]] * lenx)

    # Draw painted sections
    for pos in coords:
        x, y = pos
        arr[y-miny][x-minx] = COLOUR[coords[pos]]
    return arr[::-1]


def part1():
    computer = IntcodeComputer(PROGRAM, input_fifo=[], signals=True)
    visited = get_coords(computer, {})
    if __name__ == "__main__":
        pattern = get_map(visited)
        for line in pattern:
            print("".join(line))
    return len(visited)


def part2():
    """."""

    computer = IntcodeComputer(PROGRAM, input_fifo=[], signals=True)
    visited = get_coords(computer, {(0, 0): WHITE})
    if __name__ == "__main__":
        pattern = get_map(visited)
        for line in pattern:
            print("".join(line))
    return len(visited)


if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}\n")
    print(f"\n    Part 2\n    {part2()}\n")
