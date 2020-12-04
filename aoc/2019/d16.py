from itertools import repeat, chain, islice, cycle, accumulate
from time import perf_counter

from aocd import data
from aocd.models import Puzzle


def pat(base, i):
    yield from islice(cycle(tuple(chain(*(repeat(j, i + 1) for j in base)))), 1, None)


def phase(sig, base=(0, 1, 0, -1)):
    # slower
    return tuple(abs(sum(a * b for (a, b) in zip(pat(base, i), sig))) % 10 for i in range(len(sig)))


def pat0(i, sig, s=None):
    idx = s or i
    n = len(sig)
    while idx < n:
        yield from sig[idx:idx + i + 1]
        idx += i + 1 + (3 * (i + 1))


def phase0(sig):
    return tuple(abs(sum(pat0(i, sig)) - sum(pat0(i, sig, 3 * (i + 1) - 1))) % 10 for i in range(len(sig)))
    # slower
    # N = len(sig)
    # return tuple(abs(sum( (0,1,0,-1)[(i+1)//(k+1)%4]*sig[i] for i in range(N) )) % 10 for k in range(N))
    # return tuple(abs(sum(sum(sig[i::(k+1)*4]) - sum(sig[i+2*(k+1)::(k+1)*4]) for k in range(i+1))) %10 for i in range(len(sig)))


# data = '80871224585914546619083218645595'
# data = '03036732577212944063491565474664'
# data = '12345678'
# data = '02935109699940807407585447034323'

def main(*_):
    t = perf_counter()

    sig = [int(d) for d in data.strip()]
    fft = sig
    for i in range(100):
        fft = phase0(fft)
    part_a = "".join(str(d) for d in fft[:8])
    print(f'part 1: {part_a}')
    # 10189359

    off = int(data[:7])
    n = len(sig)
    sig = sig * 10000
    # upper triangular, ones matrix, don't care about anything before offset, and everything else is summed
    fft = reversed(sig[off:])
    for i in range(100):
        fft = (n % 10 for n in accumulate(fft))
        # fft = accumulate(fft, lambda a, b: (a + b) % 10)
    fft = reversed(tuple(fft)[-8:])
    part_b = "".join(str(d) for d in fft)
    print('part 2: ', part_b)
    # 80722126

    print(f'{perf_counter() - t:.2f}s')
    return part_a, part_b


if __name__ == '__main__':
    main()

    print(Puzzle(2019, 16).answers)
