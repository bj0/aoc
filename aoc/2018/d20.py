from collections import deque

import networkx

with open('d20.txt', 'rt') as f:
    input = f.read().strip()

inp = """
^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$
""".strip()


def parse(input):
    # rooms = defaultdict(set)
    maze = networkx.Graph()

    path = deque(input[1:])

    def scan(starts):
        locs = starts
        ends = set()
        while path:
            c = path.popleft()
            if c == '|':
                # split
                ends.update(locs)
                locs = starts
            elif c in ')$':
                # yield locs | ends
                # yield from locs | ends
                # return
                return locs | ends
            elif c == '(':
                # new sub
                # locs = next(scan(locs))
                # locs = {l for l in scan(locs)}
                locs = scan(locs)
            else:
                dir = DIR[c]
                maze.add_edges_from((p, p + dir) for p in locs)
                locs = {p + dir for p in locs}

    # next(scan({0 + 0j}))
    # for l in scan({0 + 0j}):
    #     pass
    scan({0 + 0j})
    return maze


DIR = {
    'N': 1j,
    'E': 1,
    'S': -1j,
    'W': -1,
}


def explore(input):
    rooms = parse(input)
    print(f'rooms:{rooms.number_of_nodes()}')
    paths = networkx.algorithms.shortest_path_length(rooms, 0)
    print(f'part1: {max(paths.values())}')
    print(f'part2: {sum(1 for s in paths.values() if s >= 1000)}')


import time

t = time.perf_counter()

# explore(inp)
# explore("""^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$""")
# explore("""^NNNNN(EEEEE|NNN)NNNNN$""")

explore(input)

print(f'{time.perf_counter() - t}s')
