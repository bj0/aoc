from collections import Counter

from aocd import data

jolts = [0, *(jolts := sorted(int(x) for x in data.splitlines())), max(jolts) + 3]

dJ = Counter(jolts[i] - jolts[i - 1] for i in range(1, len(jolts)))

# 2080
print(f'part1: {dJ[1] * dJ[3]}')
# submit(dJ[1] * dJ[3], reopen=False)

