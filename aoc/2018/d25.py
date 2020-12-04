import fileinput

import networkx as nx


def dist(p1, p2):
    return sum(abs(a - b) for a, b in zip(p1, p2))


def solve(input):
    pts = set()
    graph = nx.Graph()
    for line in input:
        pt = tuple(map(int, line.split(',')))
        graph.add_node(pt)  # for single stars
        for p in pts:
            if dist(p, pt) <= 3:
                graph.add_edge(p, pt)

        pts.add(pt)

    print('g', nx.number_connected_components(graph))

    # C = []
    # for pt in sorted(pts):
    #     added = False
    #     for c in C:
    #         if any(dist(p, pt) <= 3 for p in c):
    #             c.add(pt)
    #             added = True
    #     if not added:
    #         C.append(set([pt]))

    # check for dupes (old way)
    # dq = deque(C)
    # C = []
    # while dq:
    #     c = dq.pop()
    #     for c2 in dq:
    #         if c & c2:
    #             dq.remove(c2)
    #             c |= c2
    #             dq.append(c)
    #             break
    #     else:
    #         C.append(c)
    #
    # print(len(C))


input = fileinput.input('d25.txt')

inp = """
-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0
""".strip().splitlines()

solve(inp)

inp = """
1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2""".strip().splitlines()

solve(inp)

solve(input)
