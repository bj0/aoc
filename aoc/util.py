from functools import wraps
from time import perf_counter


def mdist(p0, p1):
    if isinstance(p0, complex) or isinstance(p1, complex):
        p0, p1 = complex(p0), complex(p1)
        return mdist((p0.real, p0.imag), (p1.real, p1.imag))
    return sum(abs(a - b) for a, b in zip(p0, p1))


def doublewrap(f):
    '''
    a decorator decorator, allowing the decorator to be used as:
    @decorator(with, arguments, and=kwargs)
    or
    @decorator
    '''

    @wraps(f)
    def new_dec(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            # actual decorated function
            return f(args[0])
        else:
            # decorator arguments
            return lambda realf: f(realf, *args, **kwargs)

    return new_dec


# @doublewrap
def perf(f):
    """print a line showing how long it took this function to run"""

    def fmt(num):
        for tol, f, suf in ((1, 1, 's'), (1e-3, 1e3, 'ms'), (1e-6, 1e6, '\xb5s')):
            if num > tol:
                return f'{num * f:.3g}{suf}'
        return f'{num:.1e}s'

    @wraps(f)
    def wrap(*args, **kwargs):
        t = perf_counter()
        ret = f(*args, **kwargs)
        print(f'<{f.__name__}> took {fmt(perf_counter() - t)}')
        return ret

    return wrap
