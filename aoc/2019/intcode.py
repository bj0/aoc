from enum import Enum

import trio


class Command(Enum):
    INPUT = 0


async def _get_input(input, output, prompt):
    # return await input.receive()
    # we want to ignore INPUT commands for process to process ipc
    inp = Command.INPUT
    while inp == Command.INPUT:
        try:
            inp = input.receive_nowait()
        except trio.WouldBlock:
            try:
                # signal for input if nothing is already available
                if prompt:
                    await output.send(Command.INPUT)
            except trio.BrokenResourceError:
                raise Exception("input closed")
            inp = await input.receive()
    return inp


async def execute_instruction(idx, mem, input, output, prompt=True):
    """
    Execute a single intcode instruction/opcode
    """
    op = mem[idx]
    if op == 99:  # halt
        # print('halt')
        return None

    # op modes (0 = address, 1 = immediate, 2 = relative)
    ma = op // 100 % 10
    mb = op // 1000 % 10
    mc = op // 10000 % 10
    op = op % 100

    def get_addr(m, a):
        """
        get address of parameter based on mode
        """
        return a if m == 0 else (a + mem['rb'])

    def get(m, a):
        """
        get value of parameter based on mode
        """
        return a if m == 1 else mem.get(get_addr(m, a), 0)

    if op == 1:  # add
        a, b, c = (mem[i] for i in range(idx + 1, idx + 4))
        r = get(ma, a) + get(mb, b)
        c = get_addr(mc, c)
        return idx + 4, {**mem, c: r}
    elif op == 2:  # mult
        a, b, c = (mem[i] for i in range(idx + 1, idx + 4))
        c = get_addr(mc, c)
        r = get(ma, a) * get(mb, b)
        return idx + 4, {**mem, c: r}
    elif op == 3:  # input
        a = mem[idx + 1]
        a = get_addr(ma, a)
        inp = await _get_input(input, output, prompt)
        return idx + 2, {**mem, a: inp}
    elif op == 4:  # output
        a = mem[idx + 1]
        a = get(ma, a)
        await output.send(a)
        return idx + 2, mem
    elif op == 5:  # not zero
        a, b = mem[idx + 1], mem[idx + 2]
        a = get(ma, a)
        b = get(mb, b)
        return b if a != 0 else (idx + 3), mem
    elif op == 6:  # zero
        a, b = mem[idx + 1], mem[idx + 2]
        a = get(ma, a)
        b = get(mb, b)
        return b if a == 0 else (idx + 3), mem
    elif op == 7:  # lt
        a, b, c = (mem[i] for i in range(idx + 1, idx + 4))
        a = get(ma, a)
        b = get(mb, b)
        c = get_addr(mc, c)
        return idx + 4, {**mem, c: (1 if a < b else 0)}
    elif op == 8:  # eq
        a, b, c = (mem[i] for i in range(idx + 1, idx + 4))
        a = get(ma, a)
        b = get(mb, b)
        c = get_addr(mc, c)
        return idx + 4, {**mem, c: (1 if a == b else 0)}
    elif op == 9:  # relative base
        a = mem[idx + 1]
        a = get(ma, a)
        r = mem['rb']
        return idx + 2, {**mem, 'rb': r + a}
    else:
        raise Exception(f"invalid op: {op}")


async def _process(memory, input=None, output=None, prompt=False):
    program = memory
    idx = 0
    while nxt := await execute_instruction(idx, program, input, output, prompt):
        idx, program = nxt

    return program


async def process(memory, input=None, output=None, prompt=True):
    """
    Process the intcode in memory to completion, taking input from the input channel and putting output on the
    output channel.  Channels are awaited and closed once the process finishes.
    """
    if input is None or output is None:
        return await _process(memory)

    async with output, input:
        # execute_instruction returns None on halt
        return await _process(memory, input, output, prompt)


def init(data, rb=0):
    """
    Convert a raw intcode program list into memory that can be processed (including relative base)
    """
    memory = {i: int(data[i]) for i in range(len(data))}
    memory['rb'] = rb
    return memory


def send_ascii(chan, line):
    """
    Send a line of ascii as ord codes to the input channel.  For this to work the channel must have a buffer,
    nowait is used.
    """
    for c in line:
        chan.send_nowait(ord(c))
    if c != '\n':
        chan.send_nowait(10)


async def recv_ascii(chan):
    line = ''
    while line[-1] != '\n':
        line += chr(await chan.recv())

    return line[:-1]


async def irecv_ascii(chan):
    """
    Wrap an output channel in an async generator that yields full ascii lines.  Input requests are passed through as
    they come in.
    """
    line = ''
    async for c in chan:
        if c == Command.INPUT:
            yield c
        elif c > 255:
            yield c
        elif c == 10:
            yield line
            line = ''
        else:
            line += chr(c)
    # chan closed
    if line:
        yield line
