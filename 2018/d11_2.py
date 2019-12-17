import numpy

serial = 8141


def power(x, y):
    rack = (x + 1) + 10
    power = rack * (y + 1)
    power += serial
    power *= rack
    return (power // 100 % 10) - 5


grid = numpy.fromfunction(power, (300, 300))

mx = 0
mxs = None
for width in range(3, 300):
    windows = sum(grid[x:x - width, y:y - width] for x in range(width) for y in range(width))
    maximum = int(windows.max())
    location = numpy.where(windows == maximum)
    if width == 3 or maximum > mx:
        mx = maximum
        mxs = (width, maximum, location[0][0] + 1, location[1][0] + 1)
        print(mxs)

print()
print(mxs)
