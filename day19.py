# pylint: disable=C0114, C0116, C0103, R0914
from utils import get_input, IntcodeComputer, bfs
import re
from PIL import Image

DATA = get_input(19)
PROGRAM = list(map(int, DATA[0].split(',')))

ANSWER = """."""

def test(x,y):
    computer = IntcodeComputer(PROGRAM, input_fifo=[x,y])
    computer.execute()
    return computer.get_output()

def part1():
    d = 50 # 50x50
    n = 0 # counter
    # use a monochrome image to store array
    i = Image.new('1', (d,d))
    start = 0 # 1st column to test
    for y in range(d):
        started=False # beam not found in this row yet
        for x in range(start, d):
            p = test(x,y) # check if beam active
            if p:
                if not started:
                    start = x+1 # beam minimum start column for next row
                    started = True # beam found in this row
                i.putpixel((x,y),1) # mark beam
                n+=1
            else: # beam not found
                if started: # beam lost
                    break # next row
    #i.show()
    return n

def part2():
    d = 10000 # map dimensions
    s = 100 # santas ship size
    i = Image.new('1', (d,d))
    start = 0
    for y in range(d):
        started=False
        for x in range(start, d):
            # if beam is active left and above then skip check as it will always be true
            if i.getpixel((x,y-1)) and i.getpixel((x-1,y)):
                p=1
            else:
                # check
                p = test(x,y)
            if p:
                if not started:
                    start = x+1
                    started = True
                i.putpixel((x,y),1)
                if i.getpixel((x-s+1,y-s+1)) and i.getpixel((x-s+1,y)) and i.getpixel((x,y-s+1)):
                    #i.show() # display the tractor beam
                    #i.save("a.bmp")
                    return (x-s+1)*10000+(y-s+1) # return the answer
            else:
                if started:
                    break
                pass
    # if we reach here something went wrong! maybe more d steps needed
    i.show()
    return -1

if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}\n")
    print(f"\n    Part 2\n    {part2()}\n")
