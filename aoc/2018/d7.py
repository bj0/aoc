from collections import defaultdict

with open('d7.txt', 'rt') as f:
    input = f.read().strip().splitlines()

inp = """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
""".strip().splitlines()


def part1(input):
    steps = defaultdict(list)
    reqs = defaultdict(list)
    posts = []
    for line in input:
        pre, post = line[5], line[36]
        steps[pre].append(post)
        reqs[post].append(pre)
        posts.append(post)

    # print(steps)
    # print(reqs)
    possible = list(sorted(x for x in steps if x not in posts))
    start = possible.pop(0)
    chain = start
    possible += [x for x in steps[start] if x not in chain and all(y in chain for y in reqs[x])]
    # print(start)
    while possible:
        # print(possible)
        possible.sort()
        next = possible.pop(0)
        chain += next
        possible += [x for x in steps[next] if x not in chain and all(y in chain for y in reqs[x])]

    # print(chain)
    return chain, steps, reqs


def part2(input, p=5, dt=60):
    steps = defaultdict(list)
    reqs = defaultdict(list)
    posts = []
    for line in input:
        pre, post = line[5], line[36]
        steps[pre].append(post)
        reqs[post].append(pre)
        posts.append(post)

    t = 0
    work = {}
    possible = list(sorted(x for x in steps if x not in posts))
    starts, possible = possible[:p], possible[p:]
    times = []
    idle = p - len(starts)
    for x in starts:
        ttl = ord(x) - ord('A') + 1 + dt
        times.append(ttl)
        work[ttl] = x
    # first to finish
    t = times.pop(0)
    done = work[t]
    chain = done
    idle += 1
    possible += [x for x in steps[done] if x not in chain and all(y in chain for y in reqs[x])]
    while possible or times:
        possible.sort()

        nexts, possible = possible[:idle], possible[idle:]
        for next in nexts:
            ttl = ord(next) - ord('A') + 1 + dt
            times.append(ttl + t)
            work[ttl + t] = next
            idle -= 1

        times.sort()
        t = times.pop(0)
        done = work[t]
        chain += done
        idle += 1
        possible += [x for x in steps[done] if x not in chain and all(y in chain for y in reqs[x])]

    print(chain, t, possible, times, idle, len(chain))


# part1(inp)

# part1(input)

part2(inp, 2, 0)

# not 916
part2(input)
