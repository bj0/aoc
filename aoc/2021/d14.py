# i attempted to dedup the codes but it turns out they don't repeat

from collections import Counter, deque


def parse_input(data):
    code, rules = data.split('\n\n')
    rules = {k: v for (k, v) in (line.split(' -> ') for line in rules.split('\n'))}

    return code, rules


def check_dup(code, dup):
    idx = []
    s = code.find(dup)
    while s != -1:
        idx += (s + 1, dup[1:-1])
        code = code[:i] + code[i + len(dup) - 2:]
        s = code.find(dup, s + 2)

    return idx, code


def process(code, rules):
    idx = []

    for key, val in rules.items():
        idx += [(i + 1, val) for i in range(len(code)) if code.startswith(key, i)]
    print('s', len(idx))
    num = 0
    for i, val in sorted(idx):
        code = code[:i + num] + val + code[i + num:]
        num += 1
    return code


#
# def deduped(code, rules, dups):
#     chunks = [code]
#     for dup in reversed(sorted(dups, key=len)):
#         new = []
#         for chunk in chunks:
#             if chunk in dups:
#                 continue
#             head, *rest = chunk.split(dup)
#             new.append([head, *(dup + z for z in ([dup, x] for x in rest))])
#             if dup in chunk:
#                 print('wtf',chunk,dup, head, rest, dup in chunk)
#                 print('new',new)
#         chunks = [c for sub in new for c in sub]
#
#     new = ''
#     # print('ck',chunks)
#     for chunk in chunks:
#         if chunk in dups:
#             new += dups[chunk]
#         else:
#             new += process(chunk, rules)
#
#     return new


# def process(code, rules, dupes):
#     dcode = deque(code)
#     idx = sorted((i + 1, val)
#                  for key, val in rules.items()
#                  for i in range(len(code) - 1) if code[i] == key[0] and code[i + 1] == key[1]
#                  )
#
#     num = 0
#     for i, val in idx:
#         dcode.insert(i + num, val)
#         # print('wtf', ''.join(dcode), val, i)
#         num += 1
#
#     return ''.join(dcode)

def step(code, map):
    new = {}
    for k, v in list(code.items()):
        for n in map[k]:
            new[n] = new.get(n, 0) + v
    return new


def count(code, ends):
    ctr = {}
    for k, v in code.items():
        for c in k:
            ctr[c] = ctr.get(c, 0) + v

    return {c: (v - 1) // 2 + 1 if c in ends else (v // 2)
            for c, v in ctr.items()}


def _solve(code, ends, map, n=10):
    """first attempt"""
    t = perf_counter()
    # 10 for p1
    for i in range(n):
        print(i)
        code = process(code, rules)
        ctr = Counter(code)
        max, *_, min = ctr.most_common()
        print(max,min, max[1]-min[1])
        # dupes[code] = process(code, rules)
        # dupes[code] = deduped(code, rules, dupes)
        # code = dupes[code]
        # print(code, len(code))

    print(sum(((k[0]+v) in rules) + ((k[1]+v) in rules) for k,v in rules.items()))
    print(len(rules))

    ctr = Counter(code)
    max, *_, min = ctr.most_common()
    print(f'part 1: {max[1] - min[1]} {perf_counter() - t:.2}s')

def main(data):
    code, rules = parse_input(data)
    from time import perf_counter

    map = {c: (f'{c[0]}{v}', f'{v}{c[1]}') for c, v in rules.items()}
    # print(map)
    ends = code[0] + code[-1]
    code = {code[i:i + 2]: 1 for i in range(len(code) - 1)}
    # print(code)

    t = perf_counter()

    for i in range(10):
        code = step(code, map)
    # print(code)
    ctr = Counter(count(code,ends))


    # t = perf_counter()
    # # 10 for p1
    # for i in range(10):
    #     print(i)
    #     code = process(code, rules)
    #     ctr = Counter(code)
    #     max, *_, min = ctr.most_common()
    #     print(max,min, max[1]-min[1])
    #     # dupes[code] = process(code, rules)
    #     # dupes[code] = deduped(code, rules, dupes)
    #     # code = dupes[code]
    #     # print(code, len(code))
    #
    # print(sum(((k[0]+v) in rules) + ((k[1]+v) in rules) for k,v in rules.items()))
    # print(len(rules))
    #
    # ctr = Counter(code)
    max, *_, min = ctr.most_common()
    print(f'part 1: {max[1] - min[1]} {perf_counter() - t:.2}s')

    # 40 for p2
    # for i in range(40 - 10):
    #     print(i)
    #     dupes[code] = process(code, rules, dupes)
    #     code = dupes[code]
    #
    # ctr = Counter(code)
    # max, *_, min = ctr.most_common()
    # print(f'part 2: {max[1] - min[1]}')


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

    # main(data)
    main(test_data)
