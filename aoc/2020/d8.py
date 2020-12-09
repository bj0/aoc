from aocd import data


def parse(line, A):
    """parse and execute an op"""
    op, n = line.split()
    n = int(n)
    if op == 'acc':
        return A + n, 1
    elif op == 'nop':
        return A, 1
    elif op == 'jmp':
        return A, n
    else:
        raise ValueError(f"unknown cmd {op}")


lines = data.splitlines()


def run(lines):
    """run the program"""
    A = 0
    idx = 0
    seen = {0}
    N = len(lines)
    while True:
        A, d = parse(lines[idx], A)
        idx += d
        if idx in seen:
            # print('loop:', idx)
            return A, False
        elif idx == N:
            # print('fin', idx)
            return A, True
        seen.add(idx)


A, _ = run(lines)
# 1548
print(f'part1: {A}')

nops = [i for (i, line) in enumerate(lines) if line.split()[0] == 'nop']
jmps = [i for (i, line) in enumerate(lines) if line.split()[0] == 'jmp']

for op in nops:
    old = lines[op]
    _, n = old.split()
    lines[op] = f'jmp {n}'
    A, succ = run(lines)
    if succ:
        print('fixed!', A, op)
        break
    lines[op] = old
else:
    # print('not nop')

    for op in jmps:
        old = lines[op]
        _, n = old.split()
        lines[op] = f'nop {n}'
        A, succ = run(lines)
        if succ:
            print('fixed!', A, op)
            # 1375
            print(f'part2: {A}')
            break
        lines[op] = old
    else:
        print('not jmp')
