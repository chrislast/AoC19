# pylint: disable=C0114, C0116, C0103, R0914
from utils import get_input, IntcodeComputer, bfs
import re

DATA = get_input(25)
PROGRAM = list(map(int, DATA[0].split(',')))

# ????,  ID ,  weight    ,dead, item
# 3766, 4653,  43        ,0,    mutex
# 3629, 4659,  1052      ,0,    dark matter
# 3294, 4671,  4125      ,0,    astronaut ice cream
# 4063, 4691,  16414     ,0,    festive hat
# 3369, 4703,  31        ,1796, escape pod
# 3967, 4714,  32        ,1872, photons
# 3558, 4722,  35        ,0,    whirled peas
# 3252, 4735,  42        ,0,    coin
# 4155, 4740,  35        ,1829, infinite loop
# 3701, 4754,  4194340   ,0,    klein bottle
# 4320, 4767,  37        ,1850, molten lava
# 3508, 4779,  2097190   ,0,    pointer
# 3821, 4787,  39        ,1818, giant electromagnet

ANSWER = """
south
south
south
south
take festive hat
north
north
north
take whirled peas
north
north
take coin
north
north
west
south
west
take mutex
west
south
east
"""


def part1():
    print("Get festive hat + mutex + whirled peas + coin!!")
    #computer = IntcodeComputer(PROGRAM)
    computer = IntcodeComputer(PROGRAM, input_fifo=ANSWER)
    computer.execute()
    ans = re.search(r"You should be able to get in by typing (\d+) on the keypad at the main airlock", computer.stdout).group(1)
    # found ids in add statements and weights in program data then go heaviest first
    # santa's code
    return int(ans)

if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}\n")
