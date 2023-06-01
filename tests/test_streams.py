try:
    from src.quickAg.streams import stream, elm, even, odd
except ModuleNotFoundError:
    from quickAg.streams import stream, elm, even, odd


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
    assert list(stream.n0.eval(elm / 3).eval(int).limit(10).unique) == [0, 1, 2, 3]


def test_gen():
    assert list(stream.n.limit(5)) == [0, 1, 2, 3, 4]
    assert list(stream.n1.limit(5)) == [1, 2, 3, 4, 5]
    assert list(stream.i.limit(5)) == [0, 1, -1, 2, -2]


def test_robin():
    s0 = stream.n0.limit(4)
    s1 = stream.n1.limit(5)
    assert list(stream.robin(s0, s1)) == [0, 1, 1, 2, 2, 3, 3, 4]


def test_zip():
    s0 = stream.n0.limit(4)
    s1 = stream.n1.limit(5)
    assert list(stream.zip(s0, s1)) == [(0, 1), (1, 2), (2, 3), (3, 4)]


def test_zip_longest():
    s0 = stream.n0.limit(4)
    s1 = stream.n1.limit(5)
    assert list(stream.zip_longest(s0, s1)) == [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (None, 5),
    ]


def test_range():
    assert list(stream.range(1, 11, 3)) == [1, 4, 7, 10]


def test_count():
    assert list(stream.count(2, 3).limit(3)) == [2, 5, 8]
