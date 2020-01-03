# pylint: disable=C0114, C0116, C0103
from utils import get_input

DATA = get_input(16)
TEST = "12345678"
T1 = ("80871224585914546619083218645595" * 10, "24176176")

def patt(n, base=(0, 1, 0, -1)):
    pattern = []
    for i in base:
        pattern += [i]*(n+1)
    return pattern[1:] + [pattern[0]]

def fft(digits, turns):
    ldigits = len(digits)
    for _ in range(1, turns+1):
        new_digits = []
        for idx in range(ldigits):
            pattern = patt(idx)
            lpat = len(pattern)
            acc = 0
            for n, digit in enumerate(digits):
                acc += digit * pattern[n % lpat]
            new_digits.append(abs(acc) % 10)
        digits = new_digits
    return digits

def part1():
    # digits = [int(n) for n in list(DATA[0])]
    # digits = [int(n) for n in list(TEST)]
    digits = [int(n) for n in list(T1[0])]
    res = fft(digits, 100)
    return ''.join([str(n) for n in res[:8]])

def part2():
    pass

if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}\n")
    print(f"\n    Part 2\n    {part2()}\n")
