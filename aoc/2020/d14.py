import itertools
import re

from aocd import data

mem = {}
mask = 'X' * 36
m_and = int(mask.replace('X', '1'), 2)
m_or = int(mask.replace('X', '0'), 2)
for line in data.splitlines():
    if 'mask' in line:
        mask = line.split()[-1]
        m_and = int(mask.replace('X', '1'), 2)
        m_or = int(mask.replace('X', '0'), 2)
    else:
        addr, val = re.fullmatch(r'mem\[(\d+)\] = (\d+)', line).groups()

        mem[addr] = (int(val) & m_and) | m_or

# 7817357407588
print(f'part1: {sum(mem.values())}')

# data = """mask = 000000000000000000000000000000X1001X
# mem[42] = 100
# mask = 00000000000000000000000000000000X0XX
# mem[26] = 1"""

mem = {}
mask = ''
for line in data.splitlines():
    if 'mask' in line:
        mask = line.split()[-1]
        idxs = [1 << (35 - m.start()) for m in re.finditer('X', mask)]
        m_and = int(mask.replace('0', '1').replace('X', '0'), 2)
        m_or = int(mask.replace('X', '0'), 2)
    else:
        addr, val = re.fullmatch(r'mem\[(\d+)\] = (\d+)', line).groups()
        addr = (int(addr) & m_and) | m_or
        for add in (sum(c) for L in range(len(idxs) + 1) for c in itertools.combinations(idxs, L)):
            mem[addr + add] = int(val)

# 4335927555692
print(f'part2: {sum(mem.values())}')
