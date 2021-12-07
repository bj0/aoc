from statistics import median, mean


def main():
    from aocd import data
    # data = """16,1,2,0,4,2,7,1,2,14"""
    xs = [int(x) for x in data.split(',')]

    # brute force
    #f = min(sum(abs(x - p) for x in xs) for p in range(min(xs), max(xs)))
    p = int(median(xs))
    print(f'part 1: p={p}, f={sum(abs(x-p) for x in xs)}')

    # brute force
    #f = min(sum(abs(x-p)*(abs(x-p)+1)//2 for x in xs) for p in range(min(xs),max(xs)))
    p = int(mean(xs))
    print(f'part 2: p={p}, f={sum(abs(x-p)*(abs(x-p)+1)//2 for x in xs)}')


if __name__ == '__main__':
    main()