ops = {
    'addr': lambda r, a, b: r[a] + r[b],
    'addi': lambda r, a, b: r[a] + b,
    'mulr': lambda r, a, b: r[a] * r[b],
    'muli': lambda r, a, b: r[a] * b,
    'banr': lambda r, a, b: r[a] & r[b],
    'bani': lambda r, a, b: r[a] & b,
    'borr': lambda r, a, b: r[a] | r[b],
    'bori': lambda r, a, b: r[a] | b,
    'seti': lambda r, a, b: a,
    'setr': lambda r, a, b: r[a],
    'gtir': lambda r, a, b: 1 if a > r[b] else 0,
    'gtri': lambda r, a, b: 1 if r[a] > b else 0,
    'gtrr': lambda r, a, b: 1 if r[a] > r[b] else 0,
    'eqir': lambda r, a, b: 1 if a == r[b] else 0,
    'eqri': lambda r, a, b: 1 if r[a] == b else 0,
    'eqrr': lambda r, a, b: 1 if r[a] == r[b] else 0
}


def part1(input, init=0):
    ipr = int(input[0][4])
    instructions = []
    for line in input[1:]:
        op, *params = line.split()
        a, b, c = [int(x) for x in params]
        instructions.append((op, a, b, c))

    regs = [0] * 6
    regs[0] = init
    ip = 0
    N = len(instructions)
    count = 0
    counts = set()
    last_r1 = 0
    while 0 <= ip < N:
        regs[ipr] = ip
        op, a, b, c = instructions[ip]
        regs[c] = ops[op](regs, a, b)
        count += 1
        ip = regs[ipr] + 1
        if ip == 28:
            r1 = regs[1]
            if r1 in counts:
                print(f'repeat: {r1}, last non-repeat: {last_r1}')
                break
            last_r1 = r1
            counts.add(r1)
            # print(count, '> ', *regs)

    # print(counts)
    # ret = ops[op](regs, a, b)


with open('d21.txt', 'rt') as f:
    input = f.read().splitlines()

import time
t = time.perf_counter()

part1(input, ord('a'))

print(f'{time.perf_counter()-t}s')