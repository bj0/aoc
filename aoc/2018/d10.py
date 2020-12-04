import time

with open('d10.txt', 'rt')as f:
    input = f.read().strip().splitlines()

inp = """
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>""".strip().splitlines()


class Point:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy


def parse(input):
    points = {}
    for i, line in enumerate(input):
        # print(line)
        sline = line.split(',')
        x, y = sline[0][-6:], sline[1][:7]
        vx, vy = sline[1][-2:], sline[2][:3]
        # print(sline)
        # x, y = sline[0][-2:], sline[1][:3]
        # vx, vy = sline[1][-2:], sline[2][:3]
        x, y, vx, vy = int(x), int(y), int(vx), int(vy)
        points[i] = Point(x, y, vx, vy)

    return points


def show(points):
    minx = min(points.values(), key=lambda p: p.x).x
    miny = min(points.values(), key=lambda p: p.y).y
    maxx = max(points.values(), key=lambda p: p.x).x
    maxy = max(points.values(), key=lambda p: p.y).y

    # print(minx,miny,maxx,maxy)

    grid = [['.'] * (maxx - minx + 2) for i in range(maxy - miny + 2)]

    # print(grid)
    # print(len(points.values()))
    for p in points.values():
        grid[p.y - miny][p.x - minx] = '#'

    # print(grid)
    print('\n'.join(''.join(c for c in row) for row in grid))
    # return (maxx - minx) * (maxy - miny)


def step(points, dt=1):
    maxx = 0
    minx = 1e3
    maxy = 0
    miny = 1e3
    for p in points.values():
        p.x = p.x + p.vx*dt
        p.y = p.y + p.vy*dt
        if p.x > maxx:
            maxx = p.x
        elif p.x < minx:
            minx = p.x
        if p.y > maxy:
            maxy = p.y
        elif p.y < miny:
            miny = p.y


    return (maxx-minx)*(maxy-miny), [maxx,minx,maxy,miny]


def part1(input):
    points = parse(input)

    mx = 1e15
    tx = 0
    step(points, dt=10330)
    for t in range(300):
        show(points)
        a, z = step(points, dt=1)
        if a < mx:
            mx = a
            tx = t
            print(f't={t},a={a}')
        else:
            print(f'end>t={t},a={a}')
            break
        # time.sleep(0.5)

    print(tx, mx)


# part1(inp)

part1(input)
