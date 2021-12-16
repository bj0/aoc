# trying to understand how to use yield-from
# here i am using it as 'greenlets' for lightweight recursion
# in the alt solution, it is used to build a tree

import networkx as nx


def parse_input(data):
    g = nx.DiGraph()
    for line in data.strip().split('\n'):
        a, b = line.split('-')
        g.add_edge(a, b)
        g.add_edge(b, a)

    return g


def find_paths(g, n, seen, dup=0):
    if n == 'end':
        return [[n]]
    # assuming no big to big connections
    paths = []
    if n.islower():
        seen = seen | {n}
    for d in g.neighbors(n):
        if d == 'start': continue
        ddup = 0
        if d in seen:
            if dup < 1:
                continue
            ddup = -1
        items = yield from find_paths(g, d, seen, dup + ddup)
        paths += [[n] + path for path in items]

    return paths


def find_all_paths(g, paths, dup=0):
    # print(g.edges)
    items = yield from find_paths(g, 'start', {'start'}, dup)
    paths += items


def main():
    from aocd import data
    #     data = """start-A
    # start-b
    # A-c
    # A-b
    # b-d
    # A-end
    # b-end
    # """

    g = parse_input(data)
    paths = []
    for _ in find_all_paths(g, paths):
        pass

    # print(paths)
    print(f'part 1: {len(paths)}')

    paths = []
    for _ in find_all_paths(g, paths, 1):
        pass
    # from pprint import pprint
    # pprint(sorted(paths, key=lambda x: (x)))
    print(f'part 2: {len(paths)}')


if __name__ == '__main__':
    main()
