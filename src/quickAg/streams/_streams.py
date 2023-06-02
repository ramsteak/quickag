from __future__ import annotations
from ..math.primes import primes

from enum import Enum
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Iterator,
    Literal,
    TypeVar,
    Container,
)
from itertools import count, zip_longest
from random import random, randint
from dataclasses import dataclass


class _SFlow(Enum):
    NORM = 0
    SKIP = 1
    STOP = 2
    STAF = 3


_T = TypeVar("_T")
_R = TypeVar("_R")


@dataclass(slots=True)
class StreamResult(Generic[_T]):
    val: _T
    exc: Exception | None = None
    flw: _SFlow = _SFlow.NORM


# class StreamResult(NamedTuple, Generic[_T]):
#     val: _T
#     exc: Exception | None
#     flw: _SFlow


class Stream(Iterator[_T], Generic[_T]):
    def __init__(self, __iter: Iterable[_T], *, forceraw: bool = False):
        if isinstance(__iter, Stream) or forceraw:
            self.__iter = __iter
        else:
            self.__iter = (StreamResult(e) for e in __iter)

        self.__stack: list[Callable[[StreamResult], StreamResult]] = []
        self.__status: _SFlow = _SFlow.NORM

    def __iter__(self) -> Iterator[_T]:
        return self

    def __next__(self) -> _T:
        e = self._next_raw_()

        if e.exc is not None:
            raise e.exc
        return e.val

    def _next_raw_(self) -> StreamResult[_T]:
        if self.__status == _SFlow.STOP:
            raise StopIteration

        e = self.__iter.__next__()

        for ev in self.__stack:
            e = ev(e)
            match e.flw:
                case _SFlow.NORM:
                    continue
                case _SFlow.SKIP:
                    return self._next_raw_()
                case _SFlow.STOP:
                    raise StopIteration
                case _SFlow.STAF:
                    self.__status = _SFlow.STOP
        return e

    def _iter_raw_(self) -> Iterator[StreamResult[_T]]:
        try:
            while True:
                yield self._next_raw_()
        except StopIteration:
            return

    def filter(self, key: Callable[[_T], bool]) -> Stream[_T]:
        def w(e: StreamResult[_T]):
            if e.exc is not None:
                return e
            try:
                return StreamResult(
                    e.val, None, _SFlow.NORM if key(e.val) else _SFlow.SKIP
                )
            except Exception as exc:
                return StreamResult(e.val, exc, _SFlow.NORM)

        self.__stack.append(w)
        return self

    def filterout(self, key: Callable[[_T], bool]) -> Stream[_T]:
        def w(e: StreamResult[_T]):
            if e.exc is not None:
                return e
            try:
                return StreamResult(
                    e.val, None, _SFlow.SKIP if key(e.val) else _SFlow.NORM
                )
            except Exception as exc:
                return StreamResult(e.val, exc, _SFlow.NORM)

        self.__stack.append(w)
        return self

    def stop(self, key: Callable[[_T], bool]) -> Stream[_T]:
        def w(e: StreamResult[_T]) -> StreamResult[_T]:
            if e.exc is not None:
                return e
            try:
                return StreamResult(
                    e.val, None, _SFlow.STOP if key(e.val) else _SFlow.NORM
                )
            except Exception as exc:
                return StreamResult(e.val, exc, _SFlow.NORM)

        self.__stack.append(w)
        return self

    def stopafter(self, key: Callable[[_T], bool]) -> Stream[_T]:
        def w(e: StreamResult[_T]) -> StreamResult[_T]:
            if e.exc is not None:
                return e
            try:
                return StreamResult(
                    e.val, None, _SFlow.STAF if key(e.val) else _SFlow.NORM
                )
            except Exception as exc:
                return StreamResult(e.val, exc, _SFlow.NORM)

        self.__stack.append(w)
        return self

    def limit(self, num: int) -> Stream[_T]:
        localvars = [0]

        def w(e: StreamResult[_T]) -> StreamResult[_T]:
            if localvars[0] >= num:
                return StreamResult(e.val, None, _SFlow.STOP)
            localvars[0] += 1
            return StreamResult(e.val)

        self.__stack.append(w)
        return self

    def eval(self, func: Callable[[_T], _R]) -> Stream[_R]:
        def w(e: StreamResult[_T]) -> StreamResult[_R | None]:
            if e.exc is not None:
                return e
            try:
                return StreamResult(func(e.val))
            except Exception as exc:
                return StreamResult(None, exc, _SFlow.NORM)

        self.__stack.append(w)
        return self

    def exc(
        self, exc: type[Exception], todo: Literal["skip", "stop"] = "skip"
    ) -> Stream[_T]:
        def w(e: StreamResult[_T]) -> StreamResult[_T]:
            if isinstance(e.exc, exc):
                match todo:
                    case "skip":
                        return StreamResult(e.val, None, _SFlow.SKIP)
                    case "stop":
                        return StreamResult(e.val, None, _SFlow.STOP)
            return e

        self.__stack.append(w)
        return self

    def excg(
        self, exc: type[Exception], todo: Literal["skip", "stop"] = "skip"
    ) -> Stream[_T]:
        def w(e: StreamResult[_T]) -> StreamResult[_T]:
            do = False
            if isinstance(e.exc, ExceptionGroup):
                for x in e.exc.exceptions:
                    if isinstance(x, exc):
                        do = True
            elif isinstance(e.exc, exc):
                do = True
            if do:
                match todo:
                    case "skip":
                        return StreamResult(e.val, None, _SFlow.SKIP)
                    case "stop":
                        return StreamResult(e.val, None, _SFlow.STOP)
            return e

        self.__stack.append(w)
        return self

    @property
    def unique(self):
        cache = set[_T]()

        def w(e: StreamResult[_T]) -> StreamResult[_T]:
            if e.exc is not None:
                return e
            if e.val in cache:
                return StreamResult(e.val, None, _SFlow.SKIP)
            cache.add(e.val)
            return StreamResult(e.val)

        self.__stack.append(w)
        return self

    def call(self, func: Callable[..., _R]) -> Stream[_R]:
        def w(e: StreamResult[_T]) -> StreamResult[_R | None]:
            if e.exc is not None:
                return e
            try:
                match e.val:
                    case [[*a],{**k}] | [{**k},[*a]]:
                        return StreamResult(func(*a, **k))
                    case [*a]:
                        return StreamResult(func(*a))
                    case {**k}:
                        return StreamResult(func(**k))
                    case a:
                        return StreamResult(func(a))
            except Exception as exc:
                return StreamResult(None, exc, _SFlow.NORM)

        self.__stack.append(w)
        return self
    

    def __or__(self, out: Callable[[Iterator[_T]], Container[_T]]):
        return out(self)

    def __gt__(self, out: Callable[[Iterator[_T]], Container[_T]]):
        return out(self)


class callproperty(property):
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self.fget is not None:
            return self.fget(*args, **kwds)


class streammeta(type):
    @property
    def naturals(self) -> Stream[int]:
        return Stream(count())

    n = naturals
    n0 = naturals

    @property
    def n1(self) -> Stream[int]:
        return Stream(count(1))

    @property
    def integers(self) -> Stream[int]:
        return stream.robin(Stream(count(0, -1)), Stream(count(1, 1)))

    i = integers

    @property
    def rand(self) -> Stream[float]:
        return Stream((random() for _ in count()))

    random = rand

    @property
    def fibonacci(self) -> Stream[int]:
        def fib() -> Iterable[int]:
            a, b = 0, 1
            while True:
                yield a
                b, a = a + b, b

        return Stream(fib())

    @property
    def primes(self) -> Stream[int]:
        return Stream(primes())


class stream(metaclass=streammeta):
    def __new__(cls, __iter):
        return Stream(__iter)

    @staticmethod
    def robin(*streams: Stream[Any]):
        __iter = zip(*(s._iter_raw_() for s in streams))
        return Stream((e for es in __iter for e in es), forceraw=True)

    @staticmethod
    def robin_longest(*streams: Stream[Any]):
        __sent = object()
        __iter = zip_longest(*(s._iter_raw_() for s in streams), fillvalue=__sent)
        return Stream(
            (e for es in __iter for e in es if e is not __sent), forceraw=True
        )

    @staticmethod
    def cat(*streams: Stream[Any]) -> Stream[Any]:
        def __iter(*st):
            for s in st:
                yield from s._iter_raw_()

        return Stream(__iter(*streams), forceraw=True)

    @staticmethod
    def zip(*streams: Stream[Any]):
        def __iter(*st):
            for ts in zip(*(s._iter_raw_() for s in st)):
                exs = [e.exc for e in ts if e.exc is not None]
                if exs:
                    yield StreamResult(
                        None,
                        ExceptionGroup("Exceptions in stream iteration", exs),
                        _SFlow.NORM,
                    )
                else:
                    yield (StreamResult(tuple(t.val for t in ts)))

        return Stream(__iter(*streams), forceraw=True)

    @staticmethod
    def zip_longest(
        *streams: Stream[Any], fillvalue: Any = None
    ) -> Stream[tuple[Any, ...]]:
        fval = fillvalue = StreamResult(fillvalue)

        def __iter(*st):
            for ts in zip_longest(*(s._iter_raw_() for s in st), fillvalue=fval):
                exs = [e.exc for e in ts if e.exc is not None]
                if exs:
                    yield StreamResult(
                        None,
                        ExceptionGroup("Exceptions in stream iteration", exs),
                        _SFlow.NORM,
                    )
                else:
                    yield (StreamResult(tuple(t.val for t in ts)))

        return Stream(__iter(*streams), forceraw=True)

    @staticmethod
    def range(*args) -> Stream[int]:
        return Stream(range(*args))

    @staticmethod
    def count(*args, **kwargs) -> Stream[int]:
        return Stream(count(*args, **kwargs))

    @staticmethod
    def randint(a: int, b: int) -> Stream[int]:
        return Stream((randint(a, b) for _ in count()))
