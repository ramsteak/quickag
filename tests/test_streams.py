try:
    from src.quickAg.streams import stream, elm, even, odd
except ModuleNotFoundError:
    from quickAg.streams import stream, elm, even, odd


class ZeroError(Exception):
    ...


def x0(__v: int) -> int:
    if __v == 0:
        raise ZeroError
    return __v


def test_stream():
    assert list(stream.n0.limit(5)) == [0, 1, 2, 3, 4]


def test_filter():
    assert list(stream.n0.limit(8).filter(even)) == [0, 2, 4, 6]
    assert list(stream.n0.limit(8).filterout(odd)) == [0, 2, 4, 6]


def test_stop():
    assert list(stream.n0.filterout(elm % 3).stop(elm > 8)) == [0, 3, 6]
    assert list(stream.n0.filterout(elm % 3).stopafter(elm > 8)) == [0, 3, 6, 9]


def test_eval_exc():
    assert list(stream.n0.limit(3).eval(1 / elm).exc(ZeroDivisionError)) == [1.0, 0.5]


def test_unique():
    assert list(stream.n0.eval(elm // 3).limit(10).unique) == [0, 1, 2, 3]


def test_uniqueret():
    assert list(stream.n0.limit(5).uniqueret(elm // 3)) == [0, 3]


def test_duplicates():
    assert list(stream.n0.eval(elm // 3).limit(10).duplicates) == [0, 1, 2]


def test_collisions():
    assert list(stream.n0.limit(5).collisions(elm % 3)) == [((3, 0), 0), ((4, 1), 1)]


def test_gen():
    assert list(stream.n.limit(5)) == [0, 1, 2, 3, 4]
    assert list(stream.n1.limit(5)) == [1, 2, 3, 4, 5]
    assert list(stream.i.limit(5)) == [0, 1, -1, 2, -2]
    assert list(stream.fibonacci.limit(7)) == [0, 1, 1, 2, 3, 5, 8]
    assert list(stream.primes.limit(7)) == [2, 3, 5, 7, 11, 13, 17]


def test_robin():
    s0 = stream.n0.limit(4)
    s1 = stream.n1.limit(5)
    ss = stream.robin(s0, s1)
    assert list(ss) == [0, 1, 1, 2, 2, 3, 3, 4]


def test_robin_exc():
    s0 = stream.n1.limit(4).eval(x0)
    s1 = stream.n0.limit(5).eval(x0)
    ss = stream.robin(s0, s1).exc(ZeroError)
    assert list(ss) == [1, 2, 1, 3, 2, 4, 3]


def test_zip():
    s0 = stream.n0.limit(4)
    s1 = stream.n1.limit(5)
    ss = stream.zip(s0, s1)
    assert list(ss) == [(0, 1), (1, 2), (2, 3), (3, 4)]


def test_zip_exc():
    s0 = stream.n1.limit(4).eval(x0)
    s1 = stream.n0.limit(5).eval(x0)
    ss = stream.zip(s0, s1).excg(ZeroError)
    assert list(ss) == [(2, 1), (3, 2), (4, 3)]


def test_zip_longest():
    s0 = stream.n0.limit(4)
    s1 = stream.n1.limit(5)
    ss = stream.zip_longest(s0, s1)
    assert list(ss) == [(0, 1), (1, 2), (2, 3), (3, 4), (None, 5)]


def test_zip_longest_exc():
    s0 = stream.n1.limit(4).eval(x0)
    s1 = stream.n0.limit(5).eval(x0)
    ss = stream.zip_longest(s0, s1).excg(ZeroError)
    assert list(ss) == [(2, 1), (3, 2), (4, 3), (None, 4)]


def test_cat():
    s0 = stream.n0.limit(4)
    s1 = stream.n1.limit(5)
    ss = stream.cat(s0, s1)
    assert list(ss) == [0, 1, 2, 3, 1, 2, 3, 4, 5]


def test_cat_exc():
    s0 = stream.n1.limit(4).eval(x0)
    s1 = stream.n0.limit(5).eval(x0)
    ss = stream.cat(s0, s1).exc(ZeroError)
    assert list(ss) == [1, 2, 3, 4, 1, 2, 3, 4]


def test_range():
    assert list(stream.range(1, 11, 3)) == [1, 4, 7, 10]


def test_count():
    assert list(stream.count(2, 3).limit(3)) == [2, 5, 8]


def test_call():
    ss = stream.range(5).eval(lambda x: x + 3).eval(range).call(lambda *x: sum(x))
    assert list(ss) == [3, 6, 10, 15, 21]


def test_out():
    assert stream.n0.limit(2).list == [0, 1]
    assert stream.n0.limit(2).tuple == (0, 1)
    assert stream.n0.limit(2).set == {0, 1}
    assert stream.n0.limit(2).frozenset == frozenset((0, 1))
    assert stream.n0.limit(2).null is None

def test_recursionerror():
    assert stream.n0.eval(lambda x:0).limit(999).unique.list == [0]
