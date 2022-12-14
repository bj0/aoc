from aocd import data

from aoc.util import perf

# import networkx as nx

puz = data.split('\n')


# puz = """$ cd /
# $ ls
# dir a
# 14848514 b.txt
# 8504156 c.dat
# dir d
# $ cd a
# $ ls
# dir e
# 29116 f
# 2557 g
# 62596 h.lst
# $ cd e
# $ ls
# 584 i
# $ cd ..
# $ cd ..
# $ cd d
# $ ls
# 4060174 j
# 8033020 d.log
# 5626152 d.ext
# 7214296 k""".split("\n")


# G = nx.DiGraph()

class Node:
    def __init__(self, parent):
        self.parent = parent
        self.kids = []
        self.sz = 0


def parse_ls(lines):
    sz = 0
    for i, line in enumerate(lines):
        match line.split():
            case ["$", *_]:
                return sz, lines[i:]
            case ["dir", _]:
                pass
            case [s, file]:
                sz += int(s)
    return sz, []


def parse_lines(dir, lines, dirs):
    sz = 0
    while lines:
        [line, *lines] = lines
        match line.split():
            case ["$", "ls"]:
                s, lines = parse_ls(lines)
                sz += s
            case ["$", "cd", ".."]:
                dirs.append((dir, sz))
                return sz, lines
            case ["$", "cd", cdir]:
                s, lines = parse_lines(cdir, lines, dirs)
                sz += s
    dirs.append((dir, sz))
    return sz, lines


@perf
def part1(puz):
    dirs = []
    parse_lines("/", puz, dirs)
    return sum(sz for k, sz in dirs if k not in ['/', '?'] and sz <= 100000)


# 1427048
print(f'part1: {part1(puz)}')


@perf
def part2(puz):
    dirs = []
    parse_lines("/", puz, dirs)
    used = dirs[-1][1]
    free = 7e7 - used
    need = 3e7 - free
    return min(sz for d, sz in dirs if sz > need)


# 2940614
print(f'part2: {part2(puz)}')
