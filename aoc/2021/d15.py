import networkx as nx


def parse_input(data):
    g = nx.DiGraph()
    map = {}
    for j, line in enumerate(data.split('\n')):
        for i, c in enumerate(line[:]):
            p = (i + j * 1j)
            risk = int(c)
            map[p] = risk
            if p - 1 in map:
                g.add_edge(p - 1, p, risk=risk)
                g.add_edge(p, p - 1, risk=map[p - 1])
            if p - 1j in map:
                g.add_edge(p - 1j, p, risk=risk)
                g.add_edge(p, p - 1j, risk=map[p - 1j])

    return g, map


def expand(g, map):
    """expand 5x in both direction"""
    end = max(g.nodes, key=lambda x: (x.real, x.imag))

    w, h = int(end.real + 1), int(end.imag + 1)

    for j in range(h * 5):
        for i in range(w * 5):
            p = i + j * 1j
            if p in map: continue
            back = back if (back := (i - w + j * 1j)) in map else i + (j - h) * 1j
            risk = (map[back] % 9) + 1
            map[p] = risk
            if p - 1 in map:
                g.add_edge(p - 1, p, risk=risk)
                g.add_edge(p, p - 1, risk=map[p - 1])
            if p - 1j in map:
                g.add_edge(p - 1j, p, risk=risk)
                g.add_edge(p, p - 1j, risk=map[p - 1j])

    return g, map


def main(data):
    from time import perf_counter

    t = perf_counter()
    g, map = parse_input(data)

    start = min(g.nodes, key=lambda x: (x.real, x.imag))
    end = max(g.nodes, key=lambda x: (x.real, x.imag))

    path = nx.shortest_path(g, start, end, weight='risk')
    tot = sum(map[p] for p in path[1:])
    print(f'part 1: {tot} ({perf_counter() - t:.2}s)')

    t = perf_counter()
    g, map = expand(g, map)

    start = min(g.nodes, key=lambda x: (x.real, x.imag))
    end = max(g.nodes, key=lambda x: (x.real, x.imag))

    path = nx.shortest_path(g, start, end, weight='risk')
    tot = sum(map[p] for p in path[1:])
    print(f'part 2: {tot} ({perf_counter() - t:.2}s)')


if __name__ == '__main__':
    from aocd import data

    test_data = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""

    main(test_data.strip())
    print()
    main(data.strip())
