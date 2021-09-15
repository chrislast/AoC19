# pylint: disable=C0114, C0116, C0103
from utils import get_input

DATA = get_input(22)

# T4="""deal into new stack
# cut -2
# deal with increment 7
# cut 8
# cut -4
# deal with increment 7
# cut 3
# deal with increment 9
# deal with increment 3
# cut -1""".splitlines()

# T3="""deal with increment 7
# deal with increment 9
# cut -2""".splitlines()

# T2="""cut 6
# deal with increment 7
# deal into new stack""".splitlines()

# T1="""deal with increment 7
# deal into new stack
# deal into new stack""".splitlines()

# DATA=T3
# SIZE=10

def shuffle(SIZE):
    deck = [_ for _ in range(SIZE)]
    for cmd in DATA:
        cmdx = cmd.split()
        if cmd.startswith("deal into new stack"):
            deck = deck[::-1]
        elif cmd.startswith("deal with increment"):
            n = int(cmdx[-1])
            d = deck[:]
            for _ in range(SIZE):
                d[n*_%SIZE] = deck[_]
            deck = d
        elif cmd.startswith("cut"):
            n = int(cmdx[-1])
            deck = deck[n:] + deck[:n]
        else:
            raise RuntimeError
    return deck

def part1():
    deck = shuffle(10007)
    if 2019 in deck:
        return deck.index(2019)
    return deck


############ STOLEN CODE #######################
# https://github.com/metalim/metalim.adventofcode.2019.python/blob/master/22_cards_shuffle.ipynb

# convert rules to linear polynomial.
# (g∘f)(x) = g(f(x))
def parse(L, rules):
    a,b = 1,0
    for s in rules[::-1]:
        if s == 'deal into new stack':
            a = -a
            b = L-b-1
            continue
        if s.startswith('cut'):
            n = int(s.split(' ')[1])
            b = (b+n)%L
            continue
        if s.startswith('deal with increment'):
            n = int(s.split(' ')[3])
            z = pow(n,L-2,L) # == modinv(n,L)
            a = a*z % L
            b = b*z % L
            continue
        raise Exception('unknown rule', s)
    return a,b

# modpow the polynomial: (ax+b)^m % n
# f(x) = ax+b
# g(x) = cx+d
# f^2(x) = a(ax+b)+b = aax + ab+b
# f(g(x)) = a(cx+d)+b = acx + ad+b
def polypow(a,b,m,n):
    if m==0:
        return 1,0
    if m%2==0:
        return polypow(a*a%n, (a*b+b)%n, m//2, n)
    else:
        c,d = polypow(a,b,m-1,n)
        return a*c%n, (a*d+b)%n

def shuffle2(L, N, pos, rules):
    a,b = parse(L,rules)
    a,b = polypow(a,b,N,L)
    return (pos*a+b)%L

def part2():
    L = 119315717514047
    N = 101741582076661
    return shuffle2(L,N,2020,DATA[:])

###################################################

# def part1():
#     """Doesn't work...why??"""
#     return shuffle2(10007,1,2019,DATA[:])

if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}\n")
    print(f"\n    Part 2\n    {part2()}\n")
