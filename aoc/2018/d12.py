from collections import defaultdict

with open('d12.txt', 'rt') as f:
    input = f.read().strip().splitlines()

inp = """
#..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
""".strip().splitlines()


def parse(lines):
    rules = defaultdict(lambda: ".")
    for line in lines:
        k, v = line[:5], line[-1]
        rules[k] = v
    return rules


def part1(input, gen=20):
    seed = input[0]
    rules = parse(input[2:])

    d = 1
    seed = '...' + seed + '...'
    seen = {}
    cnt = 0
    for g in range(gen):
        if seed[3] == '#':
            seed = '...'+seed
            d += 1
        if seed[-4] == '#':
            seed = seed + '...'
            # dr += 1
        # test = seed.strip('.')
        # if test in seen:
        #     print(f' gen {seen[test][0]} repeat after {g} gens')
        #     print(test)
        #     print((g, seed.find('#')))
        #     print(seen[test])
        #     if cnt > 3:
        #         return
        #     cnt += 1
        # seen[test] = (g, seed.find('#'))
        # print(seed)
        new = list(seed)
        for i in range(3, len(seed) - 3):
            new[i] = rules[seed[i - 2:i + 3]]
        seed = ''.join(new)

    count = list((i - 3 * d) if seed[i] == '#' else 0 for i in range(len(seed)))
    print(seed)
    # print(count)
    print(sum(count))


import time

t = time.perf_counter()

# part1(inp, 30)

# part1(input)

part1(input, gen=int(121))
print(f'{time.perf_counter() - t}s')
