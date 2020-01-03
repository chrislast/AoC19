# pylint: disable=C0114, C0116, C0103
from collections import Counter, namedtuple
from utils import get_input
import math

DATA = get_input(14)
RECIPES = dict()
"""
2 LFPRM, 4 GPNQ => 2 VGZVD
1 KXFHM, 14 SJLP => 8 MGRTM
144 ORE => 3 KQKXZ
16 LNSKQ, 41 KXFHM, 1 DKTW, 1 NCPSZ, 3 ZCSB, 11 MGRTM, 19 WNJWP, 11 KRBG => 1 FUEL
"""


def get_ore(component, num):
    if component == "ORE":
        return num
    else:
        if RECIPES[component]["stock"] >= num:
            RECIPES[component]["stock"] -= num
            return 0
        else:

            RECIPES[component]["stock"] += RECIPES[component]["quantity"]
            return RECIPES[component]["quantity"] * sum([get_ore(name, quant) for name, quant in RECIPES[component].items() if name not in ("quantity", "stock")])
        print(f"{num} {component}s needs {num} * {RECIPES[component].items()}")


def part1():
    for line in DATA:
        # "1 KXFHM, 14 SJLP => 8 MGRTM"
        all_components, product = line.split("=>")
        quantity, name = product.split()
        components = all_components.split(",")
        RECIPES[name] = dict(quantity=int(quantity), stock=0)
        for component in components:
            quantity, partname = component.split()
            RECIPES[name][partname] = int(quantity)
    return get_ore('FUEL', 1)

def part2():
    pass

if __name__ == "__main__":
    print(f"\n    Part 1\n    {part1()}\n")
    print(f"\n    Part 2\n    {part2()}\n")
