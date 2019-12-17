# 59/1357 Python. I usually don't post here, but I'm really proud of my part 2 solution and all the hard work I needed to come up with it. It only took me a whole day. I actually gave up on it and went to bed because the part 2 leadboard was even full, which I've never done before. Then while spending the next day with my girlfriend's family, I just kept working on it in the background in my head (might have been nice to have some paper). I think what I came up with is a correct general solution for all inputs although I'm not totally sure it is fast enough for all inputs, but it was pretty fast for mine. I don't know if this is functionally equivalent to any others posted here, but I haven't seen anything quite like it.
# For starters, I wanted a way to intersect the range of nanobots, not just check if their ranges overlapped but actually store the intersection region. After some clues from another thread, I figured out that the range of each nanobot would be a regular octahedron. Furthermore, the intersection of two octahedron will also be an octahedron (but not necessarily a regular one, the side lengths might be different). Any octahedron (even non-regular ones) can be represented as the area between four sets of orthogonal planes. Each octahedron can be converted into an axis-aligned bounding box (AABB) in a 4D space where the coordinates are x+y+z, x-y+z, -x+y+z, and -x-y+z which more or less correspond to the distance between each plane and the parallel plane that passes through the origin. As an AABB, I can use a generalized n-dimensional AABB intersection function to easily compute the intersection between two octahedrons (which will also be an octahedron in this AABB form).
# The next thing I figured out is that I can find the manhattan distance of the closet point to the origin in one of these AABB octahedrons without actually examining any points. The first coordinate is x+y+z which is the manhattan distance from the origin to any point on the planes normal to a +x, +y, +z line (within the +x, +y, +z or -x, -y, -z quadrants). So looking at each pair of parallel planes, if the corresponding min and max coordinates have different signs then the area between those planes contains the origin (distance 0), if they have the same sign the whichever has a lower absolute value is closer to the origin and that absolute value is the distance. The only problem is that there's a chance the octahedron doesn't actually touch the quadrant in which those planes are closest. This would occur if the distance on some other axis is greater (I'm not sure exactly how to explain or prove this, but it makes intuitive sense to me), so the distance of the octahedron to the origin is the maximum of the distances of the four dimension.
# It took me most of the day just to work out that math of how to represent, intersect, and measure the distance of the octahedrons, but there's still the problem of finding the largest combination of octahedrons that have a non-empty intersection. I used Python's itertools.combinations function to iterate all possible combinations of N octahedrons, starting at N=1000 and decreasing N until I found a size that had even one combination with an overlap. But this was much too slow because there are way too many combinations. So I found a really great way to optimize this. In O(n^2), I calculate how many other octahedron each one intersects with. I want the most number of intersections possible so I sort this list of numbers of intersections descending. The nanobot with the largest number of intersections (this is not the number of bots in range of it or that it is in range of) had 992 intersections, so I can skip trying to find a combination of any size bigger than that. But I can also skip combinations of that size, because if there is going to be a combination of size N there must be at least N nanobots that intersect with at least N nanobots (including itself). So I walk down the list of number of intersections until the decreasing number of intersections and the increasing number of nanobots with that many or more intersections cross. That number of intersections is an upper-bound of the maximum number of intersections. It may actually be lower than this though if some of the nanobots that intersect with this many others intersect with some smaller groups instead of with all the others with that many connections. But it gives somewhere better to start from. So now, start with combinations of this size and decrease until you find a size with at least one intersecting combination. To speed things up further, for combinations of size N, only iterate over combinations of nanobots that intersect with at least N bots.
# Doing it this way, the slowest step was actually computing the n^2 number of intersections per nanobot. With my input, the initial N was 979, there were exactly 979 bots with at least that many connections and they happened to all intersect with each other so only one combination needed to be tested for intersection after the filtering. Here's the code:

import os.path
import re
import itertools


class Octahedron(object):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def in_range(self, point):
        distance = sum(abs(c - p) for c, p in zip(self.center, point))
        return distance <= self.radius

    @staticmethod
    def convert(point):
        axes = [[1, 1, 1],
                [-1, 1, 1],
                [1, -1, 1],
                [-1, -1, 1],
                ]
        return [sum(p * a for p, a in zip(point, axis)) for axis in axes]

    @staticmethod
    def distance(box):
        dist = 0
        for n, x in zip(box.min, box.max):
            if (n < 0) != (x < 0):
                continue
            d = min(abs(n), abs(x))
            if d > dist:
                dist = d
        return dist

    @property
    def box(self):
        return Box(self.convert(self.center[:-1] + [self.center[-1] - self.radius]),
                   self.convert(self.center[:-1] + [self.center[-1] + self.radius]))

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.center, self.radius)

    def __str__(self):
        return 'pos=<%s>, r=%d' % (','.join(str(c) for c in self.center), self.radius)


class Box(object):
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.min, self.max)

    def __repr__(self):
        return '%r - %r' % (self.min, self.max)

    def __nonzero__(self):
        return all(x >= n for n, x in zip(self.min, self.max))

    def __and__(self, other):
        new_min = [max(n1, n2) for n1, n2 in zip(self.min, other.min)]
        new_max = [min(x1, x2) for x1, x2 in zip(self.max, other.max)]
        return self.__class__(new_min, new_max)


def get_input(filename=None):
    if not filename:
        filename = os.path.splitext(os.path.basename(__file__))[0] + '.txt'
    with open(filename) as fp:
        input = fp.read().rstrip()

    return [Octahedron([x, y, z], r) for x, y, z, r in
            (map(int, re.search(r'^pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(-?\d+)$', line).groups()) for line in
             input.split('\n'))]


def part1(bots):
    strongest = max(bots, key=lambda bot: bot.radius)
    count = 0
    for bot in bots:
        count += strongest.in_range(bot.center)
    return count


def part2(bots):
    bots = [bot.box for bot in bots]

    intersecting = []
    for box in bots:
        count = 0
        for box2 in bots:
            if box & box2:
                count += 1
        intersecting.append(count)

    for n, count in enumerate(sorted(intersecting, reverse=True)):
        if n + 1 >= count:
            break

    distance = None
    for n in xrange(count, 0, -1):
        print
        'n=%d' % n
        possible_indexes = [i for i, count in enumerate(intersecting) if count >= n]
        for indexes in itertools.combinations(possible_indexes, n):
            box = bots[indexes[0]]
            for index in indexes[1:]:
                box &= bots[index]
                if not box:
                    break
            else:
                dist = Octahedron.distance(box)
                ## print 'n=%d, boxes=%r, distance=%d' % (n, indexes, dist)
                if distance is None or dist < distance:
                    distance = dist
        if distance is not None:
            return distance


if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser(usage='%prog [options] [<input.txt>]')
    options, args = parser.parse_args()
    input = get_input(*args)
    print
    part1(input)
    print
    part2(input)
