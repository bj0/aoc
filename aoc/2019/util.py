from time import perf_counter

import trio

_t = None


def perf():
    global _t
    if _t is None:
        _t = perf_counter()
    else:
        print(f'{perf_counter() - _t:.2f}s')
        _t = perf_counter()


def merge(nursery, *chans):
    """
    merge multiple trio (output) channels into a single output channel
    """
    merged_send, merged_recv = trio.open_memory_channel(0)

    async def relay(frm, to):
        async with frm, to:
            async for item in frm:
                await to.send((item, frm))

    nursery.start_soon(relay, chans[0], merged_send)
    for ch in chans[1:]:
        nursery.start_soon(relay, ch, merged_send.clone())
    return merged_recv
