import re
from math import prod

from aocd import data

split = re.split(r'\n\n', data)
rules = {}
for line in split[0].splitlines():
    field, r0, r1, r2, r3 = re.match(r'(.+): (\d+)-(\d+) or (\d+)-(\d+)', line).groups()
    rules[field] = ((int(r0), int(r1)), (int(r2), int(r3)))

invalid = []
valid = {}
for line in split[2].splitlines()[1:]:
    for i, num in enumerate(line.split(',')):
        num = int(num)
        for d0, d1 in rules.values():
            if d0[0] <= num <= d0[1] or d1[0] <= num <= d1[1]:
                valid.setdefault(i, []).append(num)
                break
        else:
            invalid.append(num)

# 28081
print(f'part1: {sum(invalid)}')

matches = {}
for i in range(len(valid)):
    for field in rules:
        d0, d1 = rules[field]
        if all(d0[0] <= num <= d0[1] or d1[0] <= num <= d1[1] for num in valid[i]):
            matches.setdefault(i, set()).add(field)

seen = set()
for i in sorted(matches, key=lambda k: len(matches[k])):
    left = matches[i] - seen
    matches[i] = left
    seen |= left

ticket = [int(i) for i in split[1].splitlines()[1].split(',')]
# 314360510573
print(f"part2: {prod(ticket[i] for i in matches if matches[i].pop().startswith('departure'))}")
