from itertools import repeat, chain, islice, cycle
from time import perf_counter

from aocd import data


def pat(base, i):
    yield from islice(cycle(tuple(chain(*(repeat(j, i + 1) for j in base)))), 1, None)


def phase(sig, base=(0, 1, 0, -1)):
    return tuple(abs(sum(a * b for (a, b) in zip(pat(base, i), sig))) % 10 for i in range(len(sig)))


def pat0(i, sig, s=None):
    idx = s or i
    n = len(sig)
    while idx < n:
        # print(sig[idx:idx+i+1],idx,i)
        yield from sig[idx:idx + i + 1]
        idx += i + 1 + (3 * (i + 1))
    # print('d')


def phase0(sig):
    return tuple(abs(sum(pat0(i, sig)) - sum(pat0(i, sig, 3 * (i + 1) - 1))) % 10 for i in range(len(sig)))


# data = '80871224585914546619083218645595'
# data = '03036732577212944063491565474664'
data = '12345678'

t = perf_counter()

sig = [int(d) for d in data.strip()]
fft = sig
for i in range(100):
    fft = phase0(fft)
print(f'part 1: {"".join(str(d) for d in fft[:8])}')
# 10189359

off = int(data[:7])
sig = sig * 10
fft = sig
# # seen = {tuple(sig)}
for i in range(5):
    fft = phase(fft)
    print("".join(str(d) for d in fft))
# #     if fft in seen:
# #         print(f'cycle at {i}')
# #         break
# #     seen.add(fft)
print(fft[off - 1:10])

print(f'{perf_counter() - t:.2f}s')
