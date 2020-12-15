from collections import Counter
from time import perf_counter

from aocd import data

jolts = [0, *(jolts := sorted(int(x) for x in data.splitlines())), max(jolts) + 3]

dJ = Counter(jolts[i] - jolts[i - 1] for i in range(1, len(jolts)))

# 2080
print(f'part1: {dJ[1] * dJ[3]}')

t = perf_counter()

tot = Counter({0: 1})
for jolt in jolts:
    for i in range(1, 4):
        tot[jolt + i] += tot[jolt]

# 6908379398144
print(f'part2: {tot[jolts[-1]]}')

print(f'{perf_counter() - t:.2f}s')
