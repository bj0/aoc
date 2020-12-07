import re
from collections import Counter
from functools import reduce

from aocd import data

p1 = sum(
    len(Counter(group.replace("\n", ""))) for group in re.split(r"\n\n", data.strip())
)
print(f"part1: {p1}")

p2 = sum(
    len(reduce(lambda a, b: a & b, (set(p) for p in group.split())))
    for group in re.split(r"\n\n", data.strip())
)
print(f"part2: {p2}")
