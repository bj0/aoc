from collections import Counter

from aocd import data

map = {}
food = set()
c = Counter()
for line in data.splitlines():
    # lst, alg = re.split(r' \(contains ', line)
    lst, alg = line.split(r' (contains ')
    lst = {i for i in lst.split()}
    c.update(lst)
    food |= lst
    for al in alg[:-1].split(', '):
        map[al] = map.get(al, lst) & lst

seen = set()
while len(seen) != len(map):
    # since we don't resort each iteration
    for al in sorted(map, key=lambda x: len(map[x])):
        left = map[al] - seen
        if len(left) == 1:
            map[al] = left
            seen |= left

unsafe = {next(iter(s)) for s in map.values()}
safe = food - unsafe

print(f'part1: {sum(c[f] for f in safe)}')

print(f'part2: \'{",".join(map[a].pop() for a in sorted(map))}\'')
