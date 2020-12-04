from collections import deque


def part1(n, search):
    recipies = [3, 7]
    a, b = 0, 1

    di = 30
    for i in range(n+10):
        tot = str(recipies[a] + recipies[b])
        recipies += [int(d) for d in tot]
        a = (a + 1 + recipies[a]) % len(recipies)
        b = (b + 1 + recipies[b]) % len(recipies)

        if i % (di-6) == 0:
            if search in ''.join(str(x) for x in recipies[-di:]):
                print('found')
                break

    # print(recipies)
    s = ''.join(str(x) for x in recipies[max(i-di,0):])
    # print(s,i,di)
    if search in s:
        idx = s.index(search)
        print(idx+max(i-di,0))
    else:
        print('no match')


# with open('d14.txt','rt') as f:
#     input = f.read().strip()
input = 440231

import time
t = time.perf_counter()

# for inp in ["59414"]:
#     part1(2330, inp)

part1(int(5e7), str(input))


print(f'{time.perf_counter() - t}s')
