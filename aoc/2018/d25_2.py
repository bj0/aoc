import networkx as netx


def get_data():
    with open("d25.txt", "r") as f:
        data = f.read().rstrip()

    return [tuple(map(int, line.split(","))) for line in data.splitlines()]


def mandist(s, t):
    return sum(abs(x - y) for x, y in zip(s, t))


def part1(points):
    g = netx.Graph()
    for point in points:
        for otherpoint in points:
            if mandist(point, otherpoint) <= 3:
                g.add_edge(point, otherpoint)

    return netx.number_connected_components(g)

print(part1(get_data()))