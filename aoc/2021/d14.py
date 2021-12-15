# i attempted to dedup the codes but it turns out they don't repeat

from collections import Counter


def parse_input(data):
    code, rules = data.split('\n\n')
    rules = {k: v for (k, v) in (line.split(' -> ') for line in rules.split('\n'))}

    return code, rules


def process(code, rules):
    idx = []

    for key, val in rules.items():
        idx += [(i + 1, val) for i in range(len(code)) if code.startswith(key, i)]
    num = 0
    for i, val in sorted(idx):
        code = code[:i + num] + val + code[i + num:]
        num += 1
    return code


def step(code, map):
    new = {}
    for k, v in list(code.items()):
        for n in map[k]:
            new[n] = new.get(n, 0) + v
    return new


def count(code, ends):
    # 3 diff ways, with for loop, with walrus trick, with reduce
    ctr = {}
    # [ctr := {**ctr, c: ctr.get(c, 0) + v} for k, v in code.items() for c in k]
    # ctr = reduce(lambda d, x: {**d, x[0]: x[1] + d.get(x[0], 0)}, ((c, v) for k, v in code.items() for c in k), {})
    for k, v in code.items():
        for c in k:
            ctr[c] = ctr.get(c, 0) + v

    return Counter({c: (v - 1) // 2 + 1 if c in ends else (v // 2)
                    for c, v in ctr.items()})


def _solve(code, rules, n=10):
    """first attempt, doesn't work for part 2"""
    # 10 for p1
    for i in range(n):
        code = process(code, rules)
        ctr = Counter(code)
        max, *_, min = ctr.most_common()

    ctr = Counter(code)
    max, *_, min = ctr.most_common()
    return max[1] - min[1], ctr


def solve(code, rules, n=10):
    """keep track of counts instead of building giant strings"""

    # map rule codes back to rules
    map = {c: (f'{c[0]}{v}', f'{v}{c[1]}') for c, v in rules.items()}
    # ends aren't double counted
    ends = code[0] + code[-1]
    # format code to counts
    c = {}
    for k in (code[i:i + 2] for i in range(len(code) - 1)):
        c[k] = c.get(k, 0) + 1
    code = c

    for i in range(n):
        code = step(code, map)
    ctr = count(code, ends)

    max, *_, min = ctr.most_common()
    return max[1] - min[1], ctr


def main(data):
    code, rules = parse_input(data)
    from time import perf_counter

    t = perf_counter()
    f, _ = _solve(code, rules)
    print(f'part 1: {f} {perf_counter() - t:.2}s')

    t = perf_counter()
    f, c = solve(code, rules, 40)
    print(f'part 2: {f} {perf_counter() - t:.2}s')

    # not 4105415017404


if __name__ == '__main__':
    from aocd import data

    test_data = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

    main(data)
    # main(test_data)
