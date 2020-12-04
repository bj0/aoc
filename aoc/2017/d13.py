def parse(input):
    map = {}
    for line in input.strip().split('\n'):
        depth, rng = [x.strip() for x in line.split(':')]
        map[int(depth)] = int(rng)
    return map


def step_fw(map, state):
    for key in state:
        pos, dir = state[key]
        rng = map[key]
        if pos == 0 and dir < 0:  # bounce start
            pos, dir = 1, 1
        elif pos == rng - 1 and dir > 0:  # bounce end
            pos, dir = rng - 2, -1
        else:  # norm move
            pos += dir

        state[key] = pos, dir


def part1(input, fail_on_caught=False, delay=0, map=None):
    map = map or parse(input)
    state = {}

    # init fw state (pos, dir)
    for key in map:
        state[key] = (0, 1)

    # start packet
    alert = 0
    pos = -1
    end = max(map.keys())

    for _ in range(delay):
        step_fw(map, state)

    while pos < end:
        # step packet
        pos += 1
        if 0 in state.get(pos, []):
            # caught
            if fail_on_caught: return -1
            alert += pos * map[pos]
        # step fw
        step_fw(map, state)

    return alert


def part2(input):
    map = parse(input)
    state = {}

    # init fw state (pos, dir)
    state = {}
    for key in map:
        state[key] = (0, 1)

    end = max(map.keys())

    def packet(delay):
        # start packet
        pos = -1

        while pos < end:
            # step packet
            pos += 1
            if 0 in state.get(pos, []):
                # caught
                yield False, delay
            # step fw
            yield
            # step_fw(map, state)
        return True, delay
        # raise Exception(f"delay {delay} worked!")

    jobs = []
    try:
        for delay in range(10000000):
            jobs.append(packet(delay))
            jobs = [job for job in jobs if next(job) is None]
            step_fw(map, state)
        print('nothing??')
    except StopIteration as e:
        return e


print(part1("""
0: 3
1: 2
4: 4
6: 4
"""))

print(part1("""
0: 5
1: 2
2: 3
4: 4
6: 6
8: 4
10: 6
12: 10
14: 6
16: 8
18: 6
20: 9
22: 8
24: 8
26: 8
28: 12
30: 12
32: 8
34: 8
36: 12
38: 14
40: 12
42: 10
44: 14
46: 12
48: 12
50: 24
52: 14
54: 12
56: 12
58: 14
60: 12
62: 14
64: 12
66: 14
68: 14
72: 14
74: 14
80: 14
82: 14
86: 14
90: 18
92: 17
"""))

print(part2("""
0: 3
1: 2
4: 4
6: 4
"""))

# 3905748
print(part2("""
0: 5
1: 2
2: 3
4: 4
6: 6
8: 4
10: 6
12: 10
14: 6
16: 8
18: 6
20: 9
22: 8
24: 8
26: 8
28: 12
30: 12
32: 8
34: 8
36: 12
38: 14
40: 12
42: 10
44: 14
46: 12
48: 12
50: 24
52: 14
54: 12
56: 12
58: 14
60: 12
62: 14
64: 12
66: 14
68: 14
72: 14
74: 14
80: 14
82: 14
86: 14
90: 18
92: 17
"""))
