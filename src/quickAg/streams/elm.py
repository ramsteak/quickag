from __future__ import annotations

import math
from collections.abc import Callable
from typing import Any, overload


class Elm:
    def __init__(self, ret: Callable[..., Any] = lambda x: x) -> None:
        self.ev = ret

    def __abs__(self) -> Elm:
        return Elm(lambda x: self.ev(x).__abs__())

    def __add__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__add__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__add__(other))

    def __and__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__and__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__and__(other))

    def __contains__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__contains__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__contains__(other))

    def __div__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__div__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__div__(other))

    def __divmod__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__divmod__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__divmod__(other))

    def __eq__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__eq__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__eq__(other))

    def __floordiv__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__floordiv__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__floordiv__(other))

    def __ge__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__ge__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__ge__(other))

    def __getattr__(self, __name: str) -> Any:
        return Elm(lambda x: self.ev(x).__getitem__(__name))

    def __getitem__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__getitem__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__getitem__(other))

    def __getslice__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__getslice__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__getslice__(other))

    def __gt__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__gt__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__gt__(other))

    def __hash__(self) -> Elm:
        return Elm(lambda x: self.ev(x).__hash__())

    def __hex__(self) -> Elm:
        return Elm(lambda x: self.ev(x).__hex__())

    def __invert__(self) -> Elm:
        return Elm(lambda x: self.ev(x).__invert__())

    def __le__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__le__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__le__(other))

    def __len__(self) -> Elm:
        return Elm(lambda x: self.ev(x).__len__())

    def __lshift__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__lshift__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__lshift__(other))

    def __lt__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__lt__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__lt__(other))

    def __missing__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__missing__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__missing__(other))

    def __mod__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__mod__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__mod__(other))

    def __mul__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__mul__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__mul__(other))

    def __ne__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__ne__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__ne__(other))

    def __neg__(self) -> Elm:
        return Elm(lambda x: self.ev(x).__neg__())

    def __oct__(self) -> Elm:
        return Elm(lambda x: self.ev(x).__oct__())

    def __or__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__or__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__or__(other))

    def __pos__(self) -> Elm:
        return Elm(lambda x: self.ev(x).__pos__())

    def __pow__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__pow__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__pow__(other))

    def __radd__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__radd__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__radd__(other))

    def __rand__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__rand__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__rand__(other))

    def __rdiv__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__rdiv__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__rdiv__(other))

    def __rdivmod__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__rdivmod__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__rdivmod__(other))

    def __repr__(self) -> Elm:
        return Elm(lambda x: self.ev(x).__repr__())

    def __rfloordiv__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__rfloordiv__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__rfloordiv__(other))

    def __rlshift__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__rlshift__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__rlshift__(other))

    def __rmod__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__rmod__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__rmod__(other))

    def __rmul__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__rmul__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__rmul__(other))

    def __ror__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__ror__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__ror__(other))

    def __rpow__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__rpow__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__rpow__(other))

    def __rrshift__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__rrshift__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__rrshift__(other))

    def __rshift__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__rshift__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__rshift__(other))

    def __rsub__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__rsub__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__rsub__(other))

    def __rtruediv__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__rtruediv__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__rtruediv__(other))

    def __rxor__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__rxor__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__rxor__(other))

    # def __setitem__(self, other) -> Elm:
    #     if isinstance(other, Elm):
    #         return Elm(lambda x: self.ev(x).__setitem__(other.ev(x)))
    #     return Elm(lambda x: self.ev(x).__setitem__(other))

    def __setslice__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__setslice__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__setslice__(other))

    def __str__(self) -> Elm:
        return Elm(lambda x: self.ev(x).__str__())

    def __sub__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__sub__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__sub__(other))

    def __truediv__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__truediv__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__truediv__(other))

    def __xor__(self, other) -> Elm:
        if isinstance(other, Elm):
            return Elm(lambda x: self.ev(x).__xor__(other.ev(x)))
        return Elm(lambda x: self.ev(x).__xor__(other))

    def __call__(self, _v):
        return self.ev(_v)


@overload
def log2(__x: float) -> float:
    ...


@overload
def log2(__x: Elm) -> Elm:
    ...


def log2(__x):
    if isinstance(__x, Elm):
        return Elm(lambda x: math.log2(x))
    return math.log2(__x)


@overload
def log1p(__x: float) -> float:
    ...


@overload
def log1p(__x: Elm) -> Elm:
    ...


def log1p(__x):
    if isinstance(__x, Elm):
        return Elm(lambda x: math.log1p(x))
    return math.log1p(__x)


@overload
def ln(__x: float) -> float:
    ...


@overload
def ln(__x: Elm) -> Elm:
    ...


def ln(__x):
    if isinstance(__x, Elm):
        return Elm(lambda x: math.log(x))
    return math.log(__x)


@overload
def log10(__x: float) -> float:
    ...


@overload
def log10(__x: Elm) -> Elm:
    ...


def log10(__x):
    if isinstance(__x, Elm):
        return Elm(lambda x: math.log10(x))
    return math.log10(__x)


@overload
def log(__x: float, base: float) -> float:
    ...


@overload
def log(__x: Elm, base: float) -> Elm:
    ...


@overload
def log(__x: float, base: Elm) -> Elm:
    ...


@overload
def log(__x: Elm, base: Elm) -> Elm:
    ...


def log(__x, base):
    if isinstance(__x, Elm) and isinstance(base, Elm):
        return Elm(lambda x: math.log(__x(x), base(x)))
    if not isinstance(__x, Elm) and isinstance(base, Elm):
        return Elm(lambda x: math.log(__x, base(x)))
    if isinstance(__x, Elm) and not isinstance(base, Elm):
        return Elm(lambda x: math.log(__x(x), base))
    return math.log(__x, base)  # type: ignore


elm = Elm()


def even(__x: int) -> bool:
    return __x % 2 == 0


def odd(__x: int) -> bool:
    return __x % 2 != 0
