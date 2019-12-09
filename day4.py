# pylint: disable=C0103, C0114, C0116, W0611

FIRST = 137683
LAST = 596253


def f1(n):
    s = str(n)
    return (
        s[0] == s[1] or
        s[1] == s[2] or
        s[2] == s[3] or
        s[3] == s[4] or
        s[4] == s[5]) and \
        s[0] <= s[1] <= s[2] <= s[3] <= s[4] <= s[5]


def part1():
    return len([x for x in range(FIRST, LAST+1) if f1(x)])


def f3(x):
    s = " " + x + " "
    for i in range(1, 6):
        if s[i] == s[i+1] and s[i] != s[i-1] and s[i] != s[i+2]:
            return True
    return False


def f2(n):
    s = str(n)
    return s[0] <= s[1] <= s[2] <= s[3] <= s[4] <= s[5] and f3(s)


def part2():
    return len([x for x in range(FIRST, LAST+1) if f2(x)])


if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}")
    print(f"\n    Part 2\n    {part2()}")
