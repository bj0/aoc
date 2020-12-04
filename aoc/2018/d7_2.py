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
    reqs = defaultdict(int)
    posts = []
    for line in input:
        pre, post = line[5], line[36]
        steps[pre].append(post)
        reqs[post] += 1
        posts.append(post)

    possible = [s for s in steps if reqs[s] == 0]
    chain = ''
    while possible:
        possible.sort()
        next = possible.pop(0)
        chain += next
        for s in steps[next]:
            reqs[s] -= 1
            if reqs[s] == 0:
                possible.append(s)

    print(chain)


def part2(input, p=5, dt=60):
    steps = defaultdict(list)
    reqs = defaultdict(int)
    posts = []
    for line in input:
        pre, post = line[5], line[36]
        steps[pre].append(post)
        reqs[post] += 1
        posts.append(post)

    possible = [s for s in steps if reqs[s] == 0]
    chain = ''
    work = {}
    times = []
    idle = p
    t = 0
    while possible or times:
        possible.sort()

        # put idle workers to work
        nexts, possible = possible[:idle], possible[idle:]
        # print(nexts, idle, times, chain)
        for next in nexts:
            ttl = ord(next) - ord('A') + 1 + dt
            times.append(ttl + t)
            work[ttl + t] = next
            idle -= 1

        # next finished worker
        times.sort()
        t = times.pop(0)
        done = work[t]
        chain += done
        idle += 1
        for s in steps[done]:
            reqs[s] -= 1
            if reqs[s] == 0:
                possible.append(s)

    print(chain, t, possible, times, idle, len(chain))


part1(inp)

part1(input)

part2(inp, 2, 0)

part2(input)
