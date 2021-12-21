# i first tried to come up with an invariant i could calculate to identify matching groups of points despite coordinate system
# but i think this is too complicated and requires too many calcs
#
# maybe just assume 2 points match and calc the transform and then check to see if at least 12 overlap?
# first try takes a long time, ~8 minutes
# second try shaved about 20s off...
# got it down to ~ 5:20...
# could prob reduce it by pre-filtering by an invariant like mdist and then only checking all combinations after that
from collections import deque
from itertools import combinations, permutations, product
from math import prod

from aoc.util import perf, mdist


def parse_input(data):
    return {block.splitlines()[0]: set(tuple(int(x) for x in line.split(','))
                                       for line in block.splitlines()[1:])
            for block in data.split('\n\n')}


def remap(xs, xi, c):
    return tuple(c[i] * s for (i, s) in zip(xi, xs))


def shift(T, c):
    return tuple(t + cc for (t, cc) in zip(T, c))


def check_for_match(abeacons, bbeacons):
    for a in abeacons:
        for xs in product((1, -1), repeat=3):
            for xi in permutations((0, 1, 2), 3):
                obs = {remap(xs, xi, x) for x in bbeacons}
                for b in obs:
                    T = tuple(ac - bc for (bc, ac) in zip(b, a))
                    shifted = {shift(T, ob) for ob in obs}
                    if len(abeacons & shifted) >= 12:
                        # found a match!
                        return T, xs, xi, shifted


@perf
def part1(scanners):
    done, *waiting = scanners.items()
    beacons = done[1]
    waiting = deque(waiting)
    scanners = set()
    while waiting:
        other, other_beacons = waiting.popleft()
        print(f'trying ->{other}')
        ret = check_for_match(beacons, other_beacons)
        if ret:
            T, xs, xi, shifted = ret
            print(f' matched {other}: {xs, xi, T, len(shifted)}')
            beacons |= shifted
            scanners.add(T)
            continue
        else:
            waiting.append((other, other_beacons))
    return beacons, scanners


@perf
def part2(scanners):
    return max(mdist(a, b) for (a, b) in combinations(scanners, 2))


def main(data):
    scanners = parse_input(data)

    beacons, scanners = part1(scanners)
    print(f'part 1:{len(beacons)}')
    mx = part2(scanners)
    print(f'part 2:{mx}')


if __name__ == '__main__':
    from aocd import data

    main(data)

    test_data = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""

    main(test_data)
