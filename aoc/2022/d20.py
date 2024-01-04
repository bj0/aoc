import re
from collections import deque
from dataclasses import dataclass
from functools import reduce
from math import ceil
from multiprocessing import Pool
from operator import mul
from typing import Any

from aocd import data

from aoc.util import perf

# data = """1
# 2
# -3
# 3
# -2
# 0
# 4"""

inp = [int(x) for x in data.split("\n")]


@dataclass
class Node:
    prev: Any
    next: Any
    val: int


def nprint(head, N):
    p = head
    print(p.val, end=" ")
    while (p := p.next) is not head:
        print(p.val, end=" ")
    print()
    # p = head
    # print(p.val, end=" ")
    # while (p := p.prev) is not head:
    #     print(p.val, end=" ")
    # print()


@perf
def part1():
    N = len(inp)
    nodes = [Node(None, None, x) for x in inp]
    for n0, n1 in zip(nodes[:-1], nodes[1:]):
        n0.next, n1.prev = n1, n0
    nodes[0].prev, nodes[-1].next = nodes[-1], nodes[0]
    head = next(n for n in nodes if n.val == 0)

    for n in nodes:
        i = n.val % (N - 1)
        if i == 0:
            continue

        p = n
        for j in range(i):
            p = p.next

        n.prev.next, n.next.prev = n.next, n.prev
        p.next.prev, n.next = n, p.next
        p.next, n.prev = n, p

    nodes = []
    p = head
    for i in range(N):
        nodes.append(p)
        p = p.next

    return sum(nodes[i % N].val for i in (1000, 2000, 3000))


# 3466
print(f"part1: {part1()}")


@perf
def part2():
    key = 811589153
    N = len(inp)
    nodes = [Node(None, None, x * key) for x in inp]
    for n0, n1 in zip(nodes[:-1], nodes[1:]):
        n0.next, n1.prev = n1, n0
    nodes[0].prev, nodes[-1].next = nodes[-1], nodes[0]
    head = next(n for n in nodes if n.val == 0)

    for l in range(10):
        for n in nodes:
            i = n.val % (N - 1)
            if i == 0:
                continue

            p = n
            for j in range(i):
                p = p.next

            n.prev.next, n.next.prev = n.next, n.prev
            p.next.prev, n.next = n, p.next
            p.next, n.prev = n, p

    nodes = []
    p = head
    for i in range(N):
        nodes.append(p)
        p = p.next

    return sum(nodes[i % N].val for i in (1000, 2000, 3000))


# 9995532008348
print(f"part2: {part2()}")
