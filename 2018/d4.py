from collections import defaultdict

with open('d4.txt', 'rt') as f:
    input = f.read().strip()

inp = """
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
""".strip()


def part12(input):
    # events = parse(input)

    last_id = 0
    last_sleep = 0
    sleep = defaultdict(int)
    mins = defaultdict(int)

    for line in sorted(input.split('\n')):
        minute = int(line.split(' ')[1][:-1].split(':')[1])

        if 'begins' in line:
            last_id = f"#{line.split('#')[1].split()[0]}"
        elif 'falls' in line:
            last_sleep = minute
        elif 'wakes' in line:
            sleep[last_id] += (minute - last_sleep)
            for i in range(last_sleep, minute):
                mins[(last_id, i)] += 1

    most = max(sleep, key=lambda k: sleep[k])

    best = None
    best1 = None
    for k in mins:
        # minute slept most
        if best is None or mins[k] > mins[best]:
            best = k
        # only for id that's slept most
        if most in k and (best1 is None or mins[k] > mins[best1]):
            best1 = k

    # parts 1 and 2
    return (best1, int(best1[0][1:]) * best1[1]), (best, int(best[0][1:]) * best[1])


print(part12(inp))

print(part12(input))
