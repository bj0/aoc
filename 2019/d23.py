import math
from time import perf_counter

import intcode
import trio
from aocd import data

IDLE = object()


# wrap outputs so that we can include their address and send them all to a single channel
async def reader(i, local_out, global_out):
    async with local_out, global_out:
        async for o in local_out:
            if o == intcode.Command.INPUT:
                await global_out.send((i, IDLE))
            else:
                x = await local_out.receive()
                y = await local_out.receive()
                await global_out.send((i, (o, x, y)))


async def run(memory):
    async with trio.open_nursery() as nursery:
        ins = []
        gout_send, gout_recv = trio.open_memory_channel(0)
        for i in range(50):
            # set up channels
            in_send, in_recv = trio.open_memory_channel(10)
            out_send, out_recv = trio.open_memory_channel(0)
            # start program
            nursery.start_soon(intcode.process, memory, in_recv, out_send)
            ins.append(in_send)
            await in_send.send(i)
            nursery.start_soon(reader, i, out_recv, gout_send)

        NAT = None
        idles = [False] * 50
        last = None
        ic = 0
        async for i, data in gout_recv:
            if data == IDLE:
                idles[i] = True
                if all(idles) and NAT is not None:
                    # print('all idle')
                    idles = [False] * 50
                    ic += 1
                    await ins[0].send(NAT[0])
                    await ins[0].send(NAT[1])
                    print('ic', ic)
                    # for some reason (timing?) after sending the reset, i still get them all going idle 2x before they
                    # start sending/receiving again
                    if ic > 3:
                        ic = 0
                        print('sending', NAT)
                        if last == NAT:
                            print('double NAT:', last)
                            exit()
                last = NAT
                await ins[i].send(-1)
            else:
                ic = 0
                idles[i] = False
                addr, x, y = data
                if addr == 255:
                    NAT = (x, y)
                    continue
                await ins[addr].send(x)
                await ins[addr].send(y)


async def main():
    memory = intcode.init(data.strip().split(','))

    t = perf_counter()
    await run(memory)
    # part 1: 15969

    # part 2: 10650


trio.run(main)
