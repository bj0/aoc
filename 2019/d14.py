import re
from math import ceil

import networkx as nx
from aocd import data

#
# data = """
# 2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
# 17 NVRVD, 3 JNWZP => 8 VPVL
# 53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
# 22 VJHF, 37 MNCFX => 5 FWMGM
# 139 ORE => 4 NVRVD
# 144 ORE => 7 JNWZP
# 5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
# 5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
# 145 ORE => 6 MNCFX
# 1 NVRVD => 8 CXFTF
# 1 VJHF, 6 MNCFX => 4 RFSQX
# 176 ORE => 6 VJHF
# """
# data = """
# 171 ORE => 8 CNZTR
# 7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
# 114 ORE => 4 BHXH
# 14 VRPVC => 6 BMBT
# 6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
# 6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
# 15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
# 13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
# 5 BMBT => 4 WPTQ
# 189 ORE => 9 KTJDG
# 1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
# 12 VRPVC, 27 CNZTR => 2 XDBXC
# 15 KTJDG, 12 BHXH => 5 XCVML
# 3 BHXH, 2 VRPVC => 7 MZWV
# 121 ORE => 7 VRPVC
# 7 XCVML => 6 RJRHP
# 5 BHXH, 4 VRPVC => 5 LTCX
# """
# data = """
# 157 ORE => 5 NZVS
# 165 ORE => 6 DCFZ
# 44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
# 12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
# 179 ORE => 7 PSHF
# 177 ORE => 5 HKGWZ
# 7 DCFZ, 7 PSHF => 2 XJWVT
# 165 ORE => 2 GPVTF
# 3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
# """

g = nx.DiGraph()
reactions = {}
for line in data.strip().split('\n'):
    frm, to = line.split('=>')
    n, to = re.match(r'(\d+) (\w+)', to.strip()).groups()
    reactions[to] = [int(n)]
    for m, c in re.findall(r'(\d+) (\w+)', frm.strip()):
        reactions[to].append((int(m), c))
        g.add_edge(to, c)


# this should make sure we don't repeat reagents (using max of shortest path works on examples but fails on real input)
def longest_path(frm, to):
    if frm == to: return []
    return max(nx.all_simple_paths(g, frm, to), key=lambda p: len(p))


def ore(n=None):
    c = 'FUEL'
    n = n or reactions[c][0]
    need = {c: n}

    while len(need) > 1 or 'ORE' not in need:
        c = max(need, key=lambda c: len(longest_path(c, 'ORE')))
        n = need.pop(c)
        m, *r = reactions[c]
        f = ceil(n / m)
        for m, c in r:
            need[c] = need.get(c, 0) + f * m
    return need['ORE']


print(f'part 1: {ore()}')
# 143173

m = n = ore()
while ore(b := 1e12 // m) > 1e12:
    m += 10000
while ore(a := 1e12 // m) < 1e12:
    m -= 10000

m = int(1e12)
while (o := ore(t := (a + b) // 2)) != m:
    if b == t:
        break  # too close, can't hit exactly
    if o > m:
        a = t
    else:
        b = t

print(f'part 2: {int(t)}')
# 8845262 too high
# 8845261
# 8845252 too low
