# get aoc data and write to files
from aocd import get_data
from pathlib import Path

if __name__ == '__main__':
    for year in (2020, 2021):
        d = Path(f"{year}")
        if not d.is_dir():
            print(f"missing dir {d}")
            d.mkdir()
        print(f'doing year {year}')
        for day in range(1, 26):
            f = Path(d, f"d{day}.txt")
            if f.is_file():
                continue
            with open(f, 'wt') as io:
                print(f'writing {f}')
                io.write(get_data(day=day, year=year))
            import time

            time.sleep(1)
    print('done')
