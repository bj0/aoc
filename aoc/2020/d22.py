from aocd import data

P1, P2 = [[int(c) for c in block.splitlines()[1:]] for block in data.split('\n\n')]

p1, p2 = list(P1), list(P2)

while p1 and p2:
    c1, c2 = p1.pop(0), p2.pop(0)
    w = p1 if c1 > c2 else p2
    w.append(max(c1, c2))
    w.append(min(c1, c2))

w = p1 or p2
# 33393
print(f'part1 {sum((i * c for (i, c) in enumerate(reversed(w), 1)))}')


def play(d1, d2):
    seen = set()
    while d1 and d2:
        if (s := (tuple(d1), tuple(d2))) in seen:
            return True
        seen.add(s)
        c1, c2 = d1.pop(0), d2.pop(0)
        if c1 <= len(d1) and c2 <= len(d2):
            if play(d1[:c1], d2[:c2]):
                d1 += [c1, c2]
            else:
                d2 += [c2, c1]
        elif c1 > c2:
            d1 += [c1, c2]
        else:
            d2 += [c2, c1]

    return len(d2) == 0


p1, p2 = P1, P2

w = p1 if play(p1, p2) else p2

# 31963
print(f'part2 {sum((i * c for (i, c) in enumerate(reversed(w), 1)))}')
