import re
from collections import deque
from itertools import zip_longest
from typing import Dict

OPS = [
    'addr', 'addi',
    'mulr', 'muli',
    'banr', 'bani',
    'borr', 'bori',
    'setr', 'seti',
    'gtir', 'gtri', 'gtrr',
    'eqir', 'eqri', 'eqrr'
]


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def run_op(regs, op: str, a: int, b: int, c: int):
    if op == 'addr':
        regs[c] = regs[a] + regs[b]
    elif op == 'addi':
        regs[c] = regs[a] + b
    elif op == 'mulr':
        regs[c] = regs[a] * regs[b]
    elif op == 'muli':
        regs[c] = regs[a] * b
    elif op == 'banr':
        regs[c] = regs[a] & regs[b]
    elif op == 'bani':
        regs[c] = regs[a] & b
    elif op == 'borr':
        regs[c] = regs[a] | regs[b]
    elif op == 'bori':
        regs[c] = regs[a] | b
    elif op == 'setr':
        regs[c] = regs[a]
    elif op == 'seti':
        regs[c] = a
    elif op == 'gtir':
        regs[c] = 1 if a > regs[b] else 0
    elif op == 'gtri':
        regs[c] = 1 if regs[a] > b else 0
    elif op == 'gtrr':
        regs[c] = 1 if regs[a] > regs[b] else 0
    elif op == 'eqir':
        regs[c] = 1 if a == regs[b] else 0
    elif op == 'eqri':
        regs[c] = 1 if regs[a] == b else 0
    elif op == 'eqrr':
        regs[c] = 1 if regs[a] == regs[b] else 0

    return regs


def part1(input):
    idx = input.index('\n\n\n')
    input = input[:idx].strip().splitlines()
    count = 0
    for block in grouper(input, 4):
        regs = {k: int(v) for k, v in enumerate(block[0][9:-1].split(','))}
        out = {k: int(v) for k, v in enumerate(block[2][9:-1].split(','))}
        ins = tuple(map(int, block[1].split()))
        # print(ins)
        matches = 0
        for op in OPS:
            test = run_op(regs.copy(), op, *ins[1:])
            if test == out:
                # print(op, regs, test, out)
                matches += 1
        if matches >= 3:
            count += 1

    print(count)


def part12(input):
    *samples, _, prog = input.split('\n\n')
    insmap = {}
    instructions = {}
    count = 0
    for sample in samples:
        inp, top, out = list(list(map(int, re.findall(r'-?\d+', s))) for s in sample.splitlines())
        matches = []
        for op in OPS:
            test = run_op(list(inp), op, *top[1:])
            if test == out:
                matches.append(op)
        if len(matches) >= 3:
            count += 1

        opcode = top[0]
        prev = instructions.setdefault(opcode, set(matches))
        instructions[opcode] = prev.intersection(matches)

    print(f'part 1: {count}')

    quid = deque((k, instructions[k]) for k in sorted(instructions, key=lambda k: len(instructions[k])))
    while quid:
        k, mat = quid.popleft()
        if len(mat) == 1:
            m = mat.pop()
            assert insmap.setdefault(m, k) == k
        else:
            quid.append((k, {m for m in mat if m not in insmap}))

            if len(insmap.keys()) == len(OPS):
                break

    # print(insmap)
    lookup = {v: k for k, v in insmap.items()}

    prog = prog.strip().splitlines()
    regs = {i: 0 for i in range(4)}
    for line in prog:
        ins = tuple(map(int, line.split()))
        run_op(regs, lookup[ins[0]], *ins[1:])

    # print(f'final: {regs}')
    print(f'part 2: {regs[0]}')


with open('d16.txt', 'rt') as f:
    input = f.read()

# 640
# part1(input)
part12(input)
