from collections import Counter

from aocd import data


# data = """
# 00100
# 11110
# 10110
# 10111
# 10101
# 01111
# 00111
# 11100
# 10000
# 11001
# 00010
# 01010"""

def part1(data):
    lines = data.strip().split()
    counters = [Counter(line[i] for line in lines) for i in range(len(lines[0]))]

    gam = ''.join(c.most_common(1)[0][0] for c in counters)
    eps = ''.join(c.most_common()[-1][0] for c in counters)
    return int(gam, 2) * int(eps, 2), gam, eps


def part2(data):
    lines = data.strip().split()
    i = 0
    while len(lines) > 1:
        c = Counter(line[i] for line in lines)
        d = '0' if c['0'] > c['1'] else '1'
        lines = [line for line in lines if line[i] == d]
        i += 1
    o2 = lines[0]

    lines = data.strip().split()
    i = 0
    while len(lines) > 1:
        c = Counter(line[i] for line in lines)
        d = '1' if c['0'] > c['1'] else '0'
        lines = [line for line in lines if line[i] == d]
        i += 1
    co2 = lines[0]

    return int(o2, 2) * int(co2, 2), o2, co2


tot, gam, eps = part1(data)
print(f'part 1: g={gam},e={eps}, p = {tot}')

tot, o2, co2 = part2(data)
print(f'part 2: o2={o2}, co2={co2}, ls={tot}')
