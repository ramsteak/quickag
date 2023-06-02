from __future__ import annotations

from enum import Enum
from typing import (
    Callable,
    Generic,
    Iterable,
    Iterator,
    Literal,
    NamedTuple,
    TypeVar,
    overload,
    SupportsIndex,
)

class _SFlow(Enum):
    NORM = 0
    SKIP = 1
    STOP = 2
    STAF = 3

_T = TypeVar("_T")
_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")
_T3 = TypeVar("_T3")
_T4 = TypeVar("_T4")
_T5 = TypeVar("_T5")
_R = TypeVar("_R")
_F = TypeVar("_F")

class StreamResult(NamedTuple, Generic[_T]):
    val: _T
    exc: Exception | None
    flw: _SFlow

class Stream(Iterator[_T], Generic[_T]):
    def __init__(self, __iter: Iterable[_T]): ...
    def __iter__(self) -> Iterator[_T]: ...
    def __next__(self) -> _T: ...
    def filter(self, key: Callable[[_T], bool]) -> Stream[_T]: ...
    def filterout(self, key: Callable[[_T], bool]) -> Stream[_T]: ...
    def stop(self, key: Callable[[_T], bool]) -> Stream[_T]: ...
    def stopafter(self, key: Callable[[_T], bool]) -> Stream[_T]: ...
    def limit(self, num: int) -> Stream[_T]: ...
    def eval(self, func: Callable[[_T], _R]) -> Stream[_R]: ...
    def exc(
        self, exc: type[Exception], todo: Literal["skip", "stop"] = "skip"
    ) -> Stream[_T]: ...
    def excg(
        self, exc: type[Exception], todo: Literal["skip", "stop"] = "skip"
    ) -> Stream[_T]: ...
    @property
    def unique(self): ...
    # undocumented:
    # __init__(self, __iter, forceraw)
    # _next_raw_(self)
    # _iter_raw_(self)

class streammeta(type):
    @property
    def naturals(self) -> Stream[int]: ...
    n = naturals
    n0 = naturals
    @property
    def n1(self) -> Stream[int]: ...
    @property
    def integers(self) -> Stream[int]: ...
    i = integers
    @property
    def rand(self) -> Stream[float]: ...
    random = rand

class stream(metaclass=streammeta):
    def __new__(cls, __iter: Iterable[_T]) -> Stream[_T]: ...
    @overload
    @staticmethod
    def robin(stream1: Stream[_T1], /) -> Stream[_T1]: ...
    @overload
    @staticmethod
    def robin(stream1: Stream[_T1], stream2: Stream[_T2], /) -> Stream[_T1 | _T2]: ...
    @overload
    @staticmethod
    def robin(
        stream1: Stream[_T1], stream2: Stream[_T2], stream3: Stream[_T3], /
    ) -> Stream[_T1 | _T2 | _T3]: ...
    @overload
    @staticmethod
    def robin(
        stream1: Stream[_T1],
        stream2: Stream[_T2],
        stream3: Stream[_T3],
        stream4: Stream[_T4],
        /,
    ) -> Stream[_T1 | _T2 | _T3 | _T4]: ...
    @overload
    @staticmethod
    def robin(*streams: Stream[_T]) -> Stream[_T]: ...
    @overload
    @staticmethod
    def robin_longest(stream1: Stream[_T1], /) -> Stream[_T1]: ...
    @overload
    @staticmethod
    def robin_longest(
        stream1: Stream[_T1], stream2: Stream[_T2], /
    ) -> Stream[_T1 | _T2]: ...
    @overload
    @staticmethod
    def robin_longest(
        stream1: Stream[_T1], stream2: Stream[_T2], stream3: Stream[_T3], /
    ) -> Stream[_T1 | _T2 | _T3]: ...
    @overload
    @staticmethod
    def robin_longest(
        stream1: Stream[_T1],
        stream2: Stream[_T2],
        stream3: Stream[_T3],
        stream4: Stream[_T4],
        /,
    ) -> Stream[_T1 | _T2 | _T3 | _T4]: ...
    @overload
    @staticmethod
    def robin_longest(*streams: Stream[_T]) -> Stream[_T]: ...
    @overload
    @staticmethod
    def zip(stream1: Stream[_T1], /) -> Stream[tuple[_T1, ...]]: ...
    @overload
    @staticmethod
    def zip(
        stream1: Stream[_T1], stream2: Stream[_T2], /
    ) -> Stream[tuple[_T1 | _T2, ...]]: ...
    @overload
    @staticmethod
    def zip(
        stream1: Stream[_T1], stream2: Stream[_T2], stream3: Stream[_T3], /
    ) -> Stream[tuple[_T1 | _T2 | _T3, ...]]: ...
    @overload
    @staticmethod
    def zip(
        stream1: Stream[_T1],
        stream2: Stream[_T2],
        stream3: Stream[_T3],
        stream4: Stream[_T4],
        /,
    ) -> Stream[tuple[_T1 | _T2 | _T3 | _T4, ...]]: ...
    @overload
    @staticmethod
    def zip(*streams: Stream[_T]) -> Stream[tuple[_T, ...]]: ...
    @overload
    @staticmethod
    def zip_longest(
        stream1: Stream[_T1], /, *, fillvalue: _F = None
    ) -> Stream[tuple[_T1 | _F, ...]]: ...
    @overload
    @staticmethod
    def zip_longest(
        stream1: Stream[_T1], stream2: Stream[_T2], /, *, fillvalue: _F = None
    ) -> Stream[tuple[_T1 | _T2 | _F, ...]]: ...
    @overload
    @staticmethod
    def zip_longest(
        stream1: Stream[_T1],
        stream2: Stream[_T2],
        stream3: Stream[_T3],
        /,
        *,
        fillvalue: _F = None,
    ) -> Stream[tuple[_T1 | _T2 | _T3 | _F, ...]]: ...
    @overload
    @staticmethod
    def zip_longest(
        stream1: Stream[_T1],
        stream2: Stream[_T2],
        stream3: Stream[_T3],
        stream4: Stream[_T4],
        /,
        *,
        fillvalue: _F = None,
    ) -> Stream[tuple[_T1 | _T2 | _T3 | _T4 | _F, ...]]: ...
    @overload
    @staticmethod
    def zip_longest(
        *streams: Stream[_T], fillvalue: _F = None
    ) -> Stream[tuple[_T | _F, ...]]: ...
    @overload
    @staticmethod
    def range(__stop: SupportsIndex, /) -> Stream[int]: ...
    @overload
    @staticmethod
    def range(__start: SupportsIndex, __stop: SupportsIndex, /) -> Stream[int]: ...
    @overload
    @staticmethod
    def range(
        __start: SupportsIndex, __stop: SupportsIndex, __step: SupportsIndex, /
    ) -> Stream[int]: ...
    @overload
    @staticmethod
    def count() -> Stream[int]: ...
    @overload
    @staticmethod
    def count(start: SupportsIndex, /) -> Stream[int]: ...
    @overload
    @staticmethod
    def count(start: SupportsIndex, step: SupportsIndex, /) -> Stream[int]: ...
    @overload
    @staticmethod
    def count(*, step: SupportsIndex) -> Stream[int]: ...
    @staticmethod
    def randint(a: int, b: int) -> Stream[int]: ...
    @overload
    @staticmethod
    def cat(stream1: Stream[_T1], /) -> Stream[_T1]: ...
    @overload
    @staticmethod
    def cat(stream1: Stream[_T1], stream2: Stream[_T2], /) -> Stream[_T1 | _T2]: ...
    @overload
    @staticmethod
    def cat(
        stream1: Stream[_T1], stream2: Stream[_T2], stream3: Stream[_T3], /
    ) -> Stream[_T1 | _T2 | _T3]: ...
    @overload
    @staticmethod
    def cat(
        stream1: Stream[_T1],
        stream2: Stream[_T2],
        stream3: Stream[_T3],
        stream4: Stream[_T4],
        /,
    ) -> Stream[_T1 | _T2 | _T3 | _T4]: ...
    @overload
    @staticmethod
    def cat(*streams: Stream[_T]) -> Stream[_T]: ...
