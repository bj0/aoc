import contextlib
import io
from importlib import import_module

from aocd.models import Puzzle


def solve(year, day, data):
    prob = import_module(f'aoc.{year}.d{day}')
    with contextlib.redirect_stdout(io.StringIO()):
        return prob.main(Puzzle(year, day))
