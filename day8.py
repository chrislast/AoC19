# pylint: disable=C0114, C0116, C0103
from collections import Counter
from utils import get_input
from PIL import Image

DATA = get_input(8)[0]
HEIGHT = 6
WIDTH = 25
LAYER = HEIGHT * WIDTH


def p(txt):
    for i in range(HEIGHT):
        print(txt[i*WIDTH: i*WIDTH+WIDTH])


def part1():
    layers = []
    for i in range(int(len(DATA) / LAYER)):
        layers.append(Counter(DATA[i*LAYER: i*LAYER+LAYER]))
    zeroes = LAYER
    layer = None
    for l in layers:
        if l['0'] < zeroes:
            zeroes = l['0']
            layer = l
    return layer['1']*layer['2']


def part2():
    img = Image.new('1', (WIDTH+2, HEIGHT+2))
    layers = []
    for i in range(int(len(DATA) / LAYER)):
        layers.append(DATA[i*LAYER: i*LAYER+LAYER])

    msg = [' '] * LAYER
    for l in layers[::-1]:
        for i, c in enumerate(l):
            if c == '0':
                msg[i] = " "
                img.putpixel((i%WIDTH+1,i//WIDTH+1),0)
            elif c == '1':
                msg[i] = "#"
                img.putpixel((i%WIDTH+1,i//WIDTH+1),1)
    if __name__ == "__main__":
        p(''.join(msg))
    img.save('./images/day8p2.png')
    return ''.join(msg)


if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}\n")
    print(f"\n    Part 2\n    {part2()}\n")
