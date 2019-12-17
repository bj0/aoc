from collections import deque, defaultdict

import trio

with open('d23.txt', 'rt') as f:
    input = f.read().strip()


def parse(lines, regs):
    instructions = []
    for line in lines:
        op, reg, val = line.split()
        if reg.isdigit():
            regs[reg] = int(reg)  # use 'constant' regs for nums
        try:
            val = int(val)
            regs[val] = val
        except ValueError:
            pass
        instructions.append((op, reg, val))
    return instructions


async def worker(id, snd_chan, rcv_chan, ops, part=1):
    regs = defaultdict(int)
    regs['p'] = id
    idx = 0
    stack = deque()
    n = len(ops)
    async with snd_chan:
        async with rcv_chan:
            while 0 <= idx < n:
                op = ops[idx]
                if len(op) > 2:
                    reg, val = op[1:]
                    if isinstance(val, str):
                        val = regs[val]
                else:
                    reg = op[1]
                op = op[0]
                if op == 'set':
                    regs[reg] = val
                elif op == 'add':
                    regs[reg] += val
                elif op == 'mul':
                    regs[reg] *= val
                elif op == 'mod':
                    regs[reg] %= val
                elif op == 'snd':
                    if part == 1:
                        stack.append(regs[reg])
                    else:
                        val = int(reg) if reg.isdigit() else regs[reg]
                        # print(f'{id} puts {val}')
                        with trio.move_on_after(1) as scope:
                            await snd_chan.send(val)
                        if scope.cancelled_caught:
                            print(f"{id}'s buffer filled up!")
                            return
                elif op == 'rcv':
                    r = regs[reg]
                    if part == 2:
                        with trio.move_on_after(2) as scope:
                            regs[reg] = await rcv_chan.receive()
                            # print(f'{id} gots {regs[reg]}')
                        if scope.cancelled_caught:
                            print(f'{id} deadlocked')
                            return
                    elif r != 0:
                        regs[reg] = stack.pop()
                        # regs[reg] = await rcv_chan.receive()
                        print(f'rcv! {regs[reg]}')
                        return reg, regs[reg], idx, ops[idx]
                elif op == 'jgz':
                    cond = int(reg) if reg.isdigit() else regs[reg]
                    if cond > 0:
                        idx += val
                        continue
                idx += 1
    return regs


def part12(input, p=1):
    input = input.strip().split('\n')

    regs = defaultdict(int)
    ops = parse(input, regs)

    if p == 2:
        regs['a'] = 1

    idx = 0
    count = 0
    n = len(ops)
    seen = defaultdict(int)
    while 0 <= idx < n:
        op, reg, val = ops[idx]
        if reg == 'h':
            print('wtf!!')
        if idx == 21:
            print(f'got past! {regs["b"]},{regs["g"]},{regs["d"]},{regs}')
        elif idx == 24:
            print(f'chnk: {regs["f"]}')
        val = regs[val]
        if op == 'set':
            regs[reg] = val
        elif op == 'sub':
            regs[reg] -= val
        elif op == 'mul':
            regs[reg] *= val
            count += 1
        elif op == 'jnz':
            # if idx == 19:
            #     bc += 1
            #     if bc % 100000 == 0:
            #         print(regs[reg] % 1000)
            # cond = regs[reg]
            # reps = seen[(idx, op, cond, val)]
            # reps += 1
            # seen[(idx, op, cond, val)] = reps
            # if reps > bc:
            #     print("in a loop", (idx, op, cond, val))
            #     print(reps)
            # print(seen)

            # print(regs['h'])
            # bc -= 1
            # if bc % 100000 == 0:
            #     print(regs['h'])
            # if bc < 0:
            #     return regs['h']
            # seen.add((idx, op, cond, val))
            if regs[reg] != 0:
                idx += val
                continue
        idx += 1
    return count, regs['h'], regs


import numpy as np


def part2(n):
    count = 0
    for b in range(n, n + 17000 + 1, 17):
        s = int(np.sqrt(b))
        for d in range(2, s):
            if b % d == 0:
                # print(f'{b}|{d}')
                count += 1
                break

    return count


# print(part12(input))

# print(part12(input, 2))

print(part2(107900))
