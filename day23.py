# pylint: disable=C0114, C0116, C0103
from utils import get_input, IntcodeComputer

DATA = get_input(23)

PROGRAM = list(map(int, DATA[0].split(',')))
# print(PROGRAM)


def part1():
    """."""
    network = [IntcodeComputer(PROGRAM, input_fifo=[_], non_blocking=True) for _ in range(50)]
    while True:
        #print(".",end="")
        for nic in network:
            nic.step()
            if len(nic.output_data)==3:
                n,x,y = nic.output_data
                nic.output_data = []
                # print(f"[{nic}] -> {n} ({x},{y})")
                if n == 255:
                    return y
                network[n].add_input(x)
                network[n].add_input(y)


def part2():
    network = [IntcodeComputer(PROGRAM, input_fifo=[_], non_blocking=True) for _ in range(50)]
    lastnaty = None
    c=0
    while True:
        idle = True
        #print(".",end="")
        for nic in network:
            nic.step()
            if len(nic.output_data)==3:
                n,x,y = nic.output_data
                nic.output_data = []
                #print(f"[{nic}] -> {n} ({x},{y})")
                if n == 255:
                    natx, naty = x, y
                else:
                    network[n].add_input(x)
                    network[n].add_input(y)
            # trial and error constant representing "continuously locked"
            # all nics must receive mothing > 127 times to be really idle
            idle = idle and nic.idle > 127
        if idle:
            print(f"[{c}] NAT -> 0 ({natx},{naty})")
            if naty == lastnaty:
                return naty
            else:
                lastnaty = naty
            network[0].add_input(natx)
            network[0].add_input(naty)
            network[0].idle = 0 # reset nic 0 idle timer to prevent immediate return
        c+=1

if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}")
    print(f"\n    Part 2\n    {part2()}")

