from collections import deque, defaultdict

import trio

input = """
set i 31
set a 1
mul p 17
jgz p p
mul a 2
add i -1
jgz i -2
add a -1
set i 127
set p 826
mul p 8505
mod p a
mul p 129749
add p 12345
mod p a
set b p
mod b 10000
snd b
add i -1
jgz i -9
jgz a 3
rcv b
jgz b -1
set f 0
set i 126
rcv a
rcv b
set p a
mul p -1
add p b
jgz p 4
snd a
set a b
jgz 1 3
snd b
set f 1
add i -1
jgz i -11
snd a
jgz f -16
jgz a -19
"""


def parse(lines):
    instructions = []
    for line in lines:
        op = line.split()
        if len(op) > 2 and op[2][-1].isdigit():
            instructions.append(op[:-1] + [int(op[2])])
        else:
            instructions.append(op)
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


def part1(input):
    input = input.strip().split('\n')

    ops = parse(input)
    # print(ops)
    snd, rcv = trio.open_memory_channel(200)
    ret = trio.run(worker, 0, snd, rcv, ops)
    print(snd.statistics())
    return ret


async def part2(input):
    input = input.strip().split('\n')
    ops = parse(input)

    snd0, rcv0 = trio.open_memory_channel(200000)
    snd1, rcv1 = trio.open_memory_channel(200000)

    sndI, rcvI = trio.open_memory_channel(200000)

    count = 0
    with trio.move_on_after(120) as scope:
        async with trio.open_nursery() as nursery:
            nursery.start_soon(worker, 0, snd1, rcv0, ops, 2)
            nursery.start_soon(worker, 1, sndI, rcv1, ops, 2)
            async for i in rcvI:
                # print(f'int {i}')
                count += 1
                await snd0.send(i)
    if scope.cancelled_caught:
        print('timeout!')

    print(sndI.statistics())
    print(snd1.statistics())
    print(snd0.statistics())
    return count


print(part1("""
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""))

print(part1(input))

print(trio.run(part2, """
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d"""))

print(trio.run(part2, input))
