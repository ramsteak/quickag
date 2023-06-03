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
    Any,
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
    def filter(self, key: Callable[[_T], bool]) -> Stream[_T]:
        """
        Removes element when key(element) returns false, keeping all elements for
        which the condition is true, doing the opposite to filterout().
        """
    def filterout(self, key: Callable[[_T], bool]) -> Stream[_T]:
        """
        Removes element when key(element) returns true, keeping all elements for
        which the condition is false, doing the opposite to filter().
        """
    def stop(self, key: Callable[[_T], bool]) -> Stream[_T]:
        """
        Stops the stream when the given condition is met, without returning the
        element for which the condition is met. To obtain the element, use stopafter.
        """
    def stopafter(self, key: Callable[[_T], bool]) -> Stream[_T]:
        """
        Stops the stream when the given condition is met, returning the element
        for which the condition is met. To discard the element, use stop.
        """
    def limit(self, num: int) -> Stream[_T]:
        """
        Counts the number of items and stops the stream after the given number is
        returned.
        """
    def eval(self, func: Callable[[_T], _R]) -> Stream[_R]:
        """
        Evaluates the given function for each element of the stream, returning the
        result.
        """
    def call(self, func: Callable[..., _R]) -> Stream[_R]:
        """
        Calls the given function with the arguments from the stream. The parameters
        are extracted from the structure of the elements. It supports:
            - (1, 2) -> func(1, 2)
            - {"a": 1, "b": 2} -> func(a=2, b=3)
            - ((1, 2), "c": 3) -> func(1, 2, c=3)
        """
    def act(self, func: Callable[..., Any]) -> Stream[_T]:
        """
        Calls the given function with elements of the stream as arguments. The
        result is ignored and the original item is left in place.
        """
    def exc(
        self, exc: type[Exception], todo: Literal["skip", "stop"] = "skip"
    ) -> Stream[_T]:
        """
        If the given element has raised an exception of the given type during
        previous calculations, the method allows to ignore it and skip to the next
        element or to stop the stream completely.
        """
    def excg(
        self, exc: type[Exception], todo: Literal["skip", "stop"] = "skip"
    ) -> Stream[_T]:
        """
        If the given element has raised an exception of the given type during
        previous calculations, the method allows to ignore it and skip to the next
        element or to stop the stream completely. It also allows to check inside
        ExceptionGroups for the given exception.
        Methods that operate on streams such as zip and zip_longest will join the
        exceptions into a single ExceptionGroup.
        """
    @property
    def unique(self):
        """
        The method keeps a cache of all unique elements and returns them only if
        a new element is not contained in the cache."""
    # def __or__(self, out: Callable[[Iterable[_T]], _R]) -> _R:...
    # def __gt__(self, out: Callable[[Iterable[_T]], _R]) -> _R:...

    # UNDOCUMENTED METHODS (THEY ARE ONLY TO BE USED INTERNALLY):
    # These methods allow to operate on the StreamResults, the carrier object that
    # streams use to handle flow, values and exceptions. They are used internally
    # for methods that operate between streams, such as cat, robin and zip. They
    # are not to be used externally.
    #
    # __init__(self, __iter, forceraw)
    # The forceraw option makes so that the stream will not wrap the values into
    # StreamResults, the iterable must already be of type Iterator[StreamResult]
    #
    # _next_raw_(self)
    # The method yields the next StreamResult from the stream
    # _iter_raw_(self)
    # The method iterates on all StreamResults of the stream

class streammeta(type):
    @property
    def naturals(self) -> Stream[int]:
        """
        This factory returns a stream of all natural numbers, including zero.
        """
    @property
    def n(self) -> Stream[int]:
        """
        This factory returns a stream of all natural numbers, including zero.
        """
    @property
    def n0(self) -> Stream[int]:
        """
        This factory returns a stream of all natural numbers, including zero.
        """
    @property
    def n1(self) -> Stream[int]:
        """
        This factory returns a stream of all natural numbers, excluding zero.
        """
    @property
    def integers(self) -> Stream[int]:
        """
        This factory returns a stream of all integers, alternating between
        positive and negative values.
        """
    @property
    def i(self) -> Stream[int]:
        """
        This factory returns a stream of all integers, alternating between
        positive and negative values.
        """
    @property
    def rand(self) -> Stream[float]:
        """
        This factory returns a stream of random numbers in the range [0, 1).
        """
    @property
    def random(self) -> Stream[float]:
        """
        This factory returns a stream of random numbers in the range [0, 1).
        """
    @property
    def fibonacci(self) -> Stream[int]:
        """
        This factory returns a stream of numbers following the Fibonacci
        sequence, starting with [0, 1].
        """
    @property
    def primes(self) -> Stream[int]:
        """
        This factory returns a stream of prime numbers in order. It uses the
        iterator from quickAg.math.primes.
        """

class stream(metaclass=streammeta):
    def __new__(cls, __iter: Iterable[_T]) -> Stream[_T]: ...
    @overload
    @staticmethod
    def robin(stream1: Stream[_T1], /) -> Stream[_T1]:
        """
        The method allows to join multiple streams into a single stream by
        alternating the stream from which the value comes from. The resulting
        streams stops when the first stream ends, without returning the matching
        values from the other streams:
        stream1 : 1, 2, 3  .
        stream2 : a, b, c, d, e  .
        robin   : 1, a, 2, b, 3, c  .
        """
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
    def robin_longest(stream1: Stream[_T1], /) -> Stream[_T1]:
        """
        The method allows to join multiple streams into a single stream by
        alternating the stream from which the value comes from. The resulting
        streams continues until all values are exhausted:
        stream1       : 1, 2, 3  .
        stream2       : a, b, c, d, e  .
        robin_longest : 1, a, 2, b, 3, c, d, e  .
        """
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
    def zip(stream1: Stream[_T1], /) -> Stream[tuple[_T1, ...]]:
        """
        The method allows to join multiple streams into a single stream of tuples
        by zipping the streams together. The resulting streams stops when the
        first stream ends:
        stream1 : 1, 2, 3  .
        stream2 : a, b, c, d, e  .
        zip     : (1, a), (2, b), (3, c)  .
        """
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
    ) -> Stream[tuple[_T1 | _F, ...]]:
        """
        The method allows to join multiple streams into a single stream of tuples
        by zipping the streams together. The resulting streams continues until the
        last value is returned. The other values are filled with fillvalue:
        stream1     : 1, 2, 3  .
        stream2     : a, b, c, d, e  .
        zip_longest : (1, a), (2, b), (3, c), (None, d), (None, e)  .
        """
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
    def cat(stream1: Stream[_T1], /) -> Stream[_T1]:
        """
        The method allows to join multiple streams into a single stream by
        concatenating the streams together. The resulting stream continues until the
        last value is exhausted:
        stream1 : 1, 2, 3  .
        stream2 : a, b, c, d, e  .
        cat     : 1, 2, 3, a, b, c, d, e  .
        """
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
    @overload
    @staticmethod
    def range(__stop: SupportsIndex, /) -> Stream[int]:
        """
        The factory returns a stream of numbers dictated by the range values start,
        stop and step, identical to the builtin range function.
        """
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
    def count() -> Stream[int]:
        """
        The factory returns a stream of numbers dictated by start and step, like
        the method itertools.count.
        """
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
    def randint(a: int, b: int) -> Stream[int]:
        """
        The factory returns a stream of random integers in the range [a, b].
        """

def null(__iter: Iterable[_T]) -> None: ...
