try:
    from src.quickAg.math.primes import primes, is_prime
except ModuleNotFoundError:
    from quickAg.math.primes import primes, is_prime


def test_is_prime():
    assert is_prime(7919)


def test_primes():
    assert [2, 3, 5, 7, 11, 13, 17, 19] == [*primes(20)]
