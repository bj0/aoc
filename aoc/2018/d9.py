from collections import defaultdict, deque

input = (412, 71646)

inp = (9, 25)


#
# def part1(input):
#     players, top = input
#
#     scores = defaultdict(int)
#     p = 0
#     circle = [0]
#     idx = 0
#     for i in range(1, top + 1):
#         if i % 23 == 0:
#             tgt = (idx - 7) % len(circle)
#             scores[p + 1] += i + circle.pop(tgt)
#             idx = tgt
#         else:
#             idx = (idx + 2) % len(circle)
#             if idx > 0:
#                 circle.insert(idx, i)
#             else:
#                 circle.append(i)
#                 idx = len(circle) - 1
#         p = (p + 1) % players
#         # print(circle)
#         # print(idx)
#
#     k = max(scores, key=lambda k: scores[k])
#     print(k, scores[k])
#     # print(circle)


def play(input):
    players, top = input

    scores = defaultdict(int)
    circle = deque([0])
    for i in range(1, top + 1):
        if i % 23 == 0:
            circle.rotate(7)
            scores[i % players] += i + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(i)

    k = max(scores, key=lambda k: scores[k])
    print(k, scores[k])
    # print(circle)


play(inp)

for ex in [(10, 1618), (13, 7999), (17, 1104), (21, 6111), (30, 5807)]:
    play(ex)

print()
play(input)

import time

print()
t = time.perf_counter()
play((412, 71646 * 100))

print(f'{time.perf_counter() - t}s')
