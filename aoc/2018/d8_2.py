from collections import defaultdict

with open('d8.txt', 'rt') as f:
    input = f.read().strip()

inp = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2".strip()


def ints(input):
    return [int(x) for x in input.split()]


def parse(data):
    kids, meta = data[:2]
    p1 = 0
    value = defaultdict(int)
    data = data[2:]
    for i in range(kids):
        for data, kid, val in parse(data):
            # yield '>', kid, val
            pass
        p1 += kid
        value[i] = val

    mdata = data[:meta]
    value = sum(mdata) if kids == 0 else sum(value[i - 1] for i in mdata)
    yield data[meta:], (p1 + sum(mdata)), value


for x in parse(ints(inp)):
    print(x)

for x in parse(ints(input)):
    print(x)
