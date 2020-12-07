import queue
import re
from collections import defaultdict, deque

from aocd import data

rules = defaultdict(list)
rev = defaultdict(list)
for rule in data.splitlines():
    bag, contents = re.match(r'(.+) bags contain (.+)', rule).groups()
    for inner in contents.strip('.').split(','):
        inner = inner.strip()
        if inner == 'no other bags':
            continue
        n, col = re.match(r'(\d+) (.+) bags?', inner).groups()
        rules[bag].append((int(n), col))
        rev[col].append(bag)

q = deque(['shiny gold'])
bags = set()
while q:
    for bag in rev[q.pop()]:
        if bag in bags:
            continue
        bags.add(bag)
        q.append(bag)

# 115
print(f'part 1: {len(bags)}')


def part2(m, bag):
    # print(bag)
    return sum(m * part2(n, col) for (n, col) in rules[bag]) + m


# not 1250
print(f'part2: {part2(1, "shiny gold") - 1}')
