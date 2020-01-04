# pylint: disable=C0114, C0116, C0103
from collections import Counter, namedtuple
from utils import get_input
import math

DATA = get_input(14)
"""
2 LFPRM, 4 GPNQ => 2 VGZVD
1 KXFHM, 14 SJLP => 8 MGRTM
144 ORE => 3 KQKXZ
16 LNSKQ, 41 KXFHM, 1 DKTW, 1 NCPSZ, 3 ZCSB, 11 MGRTM, 19 WNJWP, 11 KRBG => 1 FUEL

==>

RECIPES = {
"VGZVD": {"makes":2, "used":0, "unused":0, "recipe":{"LFPRM":2, "GPNQ":4}}, ...
}
"""

RECIPES = dict(ORE={"used": 0, "unused": 0})

for line in DATA:
    # "1 KXFHM, 14 SJLP => 8 MGRTM"
    all_components, product = line.split("=>")
    quantity, name = product.split()
    components = all_components.split(",")
    RECIPES[name] = dict(makes=int(quantity), used=0, unused=0, recipe=dict())
    for component in components:
        quantity, partname = component.split()
        RECIPES[name]["recipe"][partname] = int(quantity)

def make(component, quantity):
    c = RECIPES[component]
    if component == "ORE":
        c["used"] += quantity
        return
    if c["unused"] < quantity:
        needed = math.ceil((quantity - c["unused"]) / c["makes"])
        c["unused"] += c["makes"] * needed
        for sub, csub in c["recipe"].items():
            make(sub, csub * needed)
    c["used"] += quantity
    c["unused"] -= quantity

def part1():
    make('FUEL', 1)
    return RECIPES["ORE"]["used"]

def part2():
    TOTAL_ORE = 1000000000000
    # maximum ore used to make one fuel
    ONE_FUEL = RECIPES["ORE"]["used"]
    while RECIPES["ORE"]["used"] <= TOTAL_ORE:
        # fuel made if each fuel used maximum ore
        guess = max(1, int((TOTAL_ORE - RECIPES["ORE"]["used"]) / ONE_FUEL))
        if __name__ == "__main__":
            print("    Make", guess, "more FUEL")
        make('FUEL', guess)
    return RECIPES["FUEL"]["used"]-1


if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}\n")
    print(f"\n    Part 2\n    {part2()}\n")
