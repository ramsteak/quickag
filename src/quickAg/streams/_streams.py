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
)
from itertools import count, zip_longest
from random import random, randint
from dataclasses import dataclass


class _SFlow(Enum):
    NORM = 0
    SKIP = 1
    STOP = 2
    STAF = 3
    EXCP = 4


_T = TypeVar("_T")
_R = TypeVar("_R")
_D = TypeVar("_D")


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
            self.__iter = __iter  # type: ignore
        else:
            self.__iter = (StreamResult(e) for e in __iter)
        self.__iter: Iterator[StreamResult[_T]]

        self.__stack: list[Callable[[StreamResult], StreamResult]] = []
        self.__status: _SFlow = _SFlow.NORM

    def __iter__(self) -> Iterator[_T]:
        return self

    def __next__(self) -> _T:
        e = self._next_raw_()

        if e.flw != _SFlow.NORM:
            raise RuntimeError(e)
        return e.val

    def _next_raw_(self) -> StreamResult:
        while True:
            if self.__status == _SFlow.STOP:
                raise StopIteration

            try:
                e = self.__iter.__next__()
            except StopIteration:
                e = StreamResult(None, None, _SFlow.STOP)

            for ev in self.__stack:
                e = ev(e)

            match e.flw:
                case _SFlow.SKIP:
                    continue
                case _SFlow.NORM:
                    return e
                case _SFlow.STOP:
                    raise StopIteration
                case _SFlow.STAF:
                    self.__status = _SFlow.STOP
                    return StreamResult(e.val, e.exc, _SFlow.NORM)
                case _SFlow.EXCP:
                    return e

    def _iter_raw_(self) -> Iterator[StreamResult[_T]]:
        try:
            while True:
                yield self._next_raw_()
        except StopIteration:
            return

    def filter(self, key: Callable[[_T], bool]) -> Stream[_T]:
        def w(e: StreamResult[_T]) -> StreamResult[_T]:
            match e:
                case StreamResult(val, None, _SFlow.NORM):
                    try:
                        if not key(val):
                            return StreamResult(val, None, _SFlow.SKIP)
                        return StreamResult(val)
                    except Exception as exc:
                        return StreamResult(val, exc, _SFlow.EXCP)
                case _:
                    return e

        self.__stack.append(w)
        return self

    def filterout(self, key: Callable[[_T], bool]) -> Stream[_T]:
        def w(e: StreamResult[_T]) -> StreamResult[_T]:
            match e:
                case StreamResult(val, None, _SFlow.NORM):
                    try:
                        if key(val):
                            return StreamResult(val, None, _SFlow.SKIP)
                        return StreamResult(val)
                    except Exception as exc:
                        return StreamResult(val, exc, _SFlow.EXCP)
                case _:
                    return e

        self.__stack.append(w)
        return self

    def stop(self, key: Callable[[_T], bool]) -> Stream[_T]:
        def w(e: StreamResult[_T]) -> StreamResult[_T]:
            match e:
                case StreamResult(val, None, _SFlow.NORM):
                    try:
                        if not key(val):
                            return StreamResult(val)
                        return StreamResult(val, None, _SFlow.STOP)
                    except Exception as exc:
                        return StreamResult(val, exc, _SFlow.EXCP)
                case _:
                    return e

        self.__stack.append(w)
        return self

    def stopafter(self, key: Callable[[_T], bool]) -> Stream[_T]:
        def w(e: StreamResult[_T]) -> StreamResult[_T]:
            match e:
                case StreamResult(val, None, _SFlow.NORM):
                    try:
                        if not key(val):
                            return StreamResult(val)
                        return StreamResult(val, None, _SFlow.STAF)
                    except Exception as exc:
                        return StreamResult(val, exc, _SFlow.EXCP)
                case _:
                    return e

        self.__stack.append(w)
        return self

    def limit(self, num: int) -> Stream[_T]:
        class w:
            def __init__(self, limit: int = 0) -> None:
                self.count = 0
                self.limit = limit

            def __call__(self, e: StreamResult[_T]) -> StreamResult[_T]:
                match e:
                    case StreamResult(val, None, _SFlow.NORM):
                        if self.count >= self.limit:
                            return StreamResult(val, None, _SFlow.STOP)
                        self.count += 1
                        return StreamResult(val)
                    case _:
                        return e

        self.__stack.append(w(num))
        return self

    take = limit

    def skip(self, num: int) -> Stream[_T]:
        class w:
            def __init__(self, skip: int = 0) -> None:
                self.count = 0
                self.skip = skip

            def __call__(self, e: StreamResult[_T]) -> StreamResult[_T]:
                match e:
                    case StreamResult(val, None, _SFlow.NORM):
                        self.count += 1
                        if self.count <= self.skip:
                            return StreamResult(val, None, _SFlow.SKIP)
                        return StreamResult(val)
                    case _:
                        return e

        self.__stack.append(w(num))
        return self

    def eval(self, func: Callable[[_T], _R]) -> Stream[_R]:
        def w(e: StreamResult[_T]) -> StreamResult[_R | None]:
            match e:
                case StreamResult(val, None, _SFlow.NORM):
                    try:
                        return StreamResult(func(val))
                    except Exception as exc:
                        return StreamResult(val, exc, _SFlow.EXCP)  # type: ignore
                case _:
                    return e  # type: ignore

        self.__stack.append(w)
        return self  # type: ignore

    map = eval

    def evr(
        self, funcraw: Callable[[StreamResult[_T]], StreamResult[_R]]
    ) -> Stream[_R]:
        self.__stack.append(funcraw)
        return self  # type: ignore

    def exc(
        self, exct: type[Exception], todo: Literal["skip", "stop"] = "skip"
    ) -> Stream[_T]:
        def w(e: StreamResult[_T]) -> StreamResult[_T]:
            match e:
                case StreamResult(val, exct(), _SFlow.EXCP):
                    match todo:
                        case "skip":
                            return StreamResult(val, None, _SFlow.SKIP)
                        case "stop":
                            return StreamResult(val, None, _SFlow.STOP)
                        case _:
                            return e
                case _:
                    return e

        self.__stack.append(w)
        return self

    def excg(
        self, exct: type[Exception], todo: Literal["skip", "stop"] = "skip"
    ) -> Stream[_T]:
        def w(e: StreamResult[_T]) -> StreamResult[_T]:
            do = False
            match e:
                case StreamResult(val, ExceptionGroup() as excg, _SFlow.EXCP):
                    if any(isinstance(ex, exct) for ex in excg.exceptions):
                        do = True
                case StreamResult(val, exct(), _SFlow.EXCP):
                    do = True
                case _:
                    return e

            if do:
                match todo:
                    case "skip":
                        return StreamResult(val, None, _SFlow.SKIP)
                    case "stop":
                        return StreamResult(val, None, _SFlow.STOP)
                    case _:
                        return e
            return e

        self.__stack.append(w)
        return self

    @property
    def unique(self):
        class w:
            def __init__(self) -> None:
                self.cache = set[_T]()

            def __call__(self, e: StreamResult[_T]) -> StreamResult[_T]:
                match e:
                    case StreamResult(val, None, _SFlow.NORM):
                        if val in self.cache:
                            return StreamResult(val, None, _SFlow.SKIP)
                        self.cache.add(val)
                        return StreamResult(val)
                    case _:
                        return e

        self.__stack.append(w())
        return self

    @property
    def duplicates(self):
        class w:
            def __init__(self) -> None:
                self.cache = dict[_T, int]()

            def __call__(self, e: StreamResult[_T]) -> StreamResult[_T]:
                match e:
                    case StreamResult(val, None, _SFlow.NORM):
                        if val not in self.cache:
                            self.cache[val] = 1
                            return StreamResult(val, None, _SFlow.SKIP)
                        if self.cache[val] == 1:
                            self.cache[val] += 1
                            return StreamResult(val)
                        return StreamResult(val, None, _SFlow.SKIP)
                    case _:
                        return e

        self.__stack.append(w())
        return self

    def uniqueret(self, func: Callable[[_T], Any]):
        class w:
            def __init__(self) -> None:
                self.cache = set()

            def __call__(self, e: StreamResult[_T]) -> StreamResult[_T]:
                match e:
                    case StreamResult(val, None, _SFlow.NORM):
                        try:
                            ret = func(val)
                        except Exception as exc:
                            return StreamResult(val, exc, _SFlow.EXCP)
                        if ret in self.cache:
                            return StreamResult(val, None, _SFlow.SKIP)
                        self.cache.add(ret)
                        return StreamResult(val)
                    case _:
                        return e

        self.__stack.append(w())
        return self

    def collisions(self, func: Callable[[_T], _R]) -> Stream[tuple[tuple[_T, _T], _R]]:
        class w:
            def __init__(self) -> None:
                self.cache = dict[_R, _T]()

            def __call__(
                self, e: StreamResult[_T]
            ) -> StreamResult[tuple[tuple[_T, _T], _R]]:
                match e:
                    case StreamResult(val, None, _SFlow.NORM):
                        try:
                            ret = func(val)
                        except Exception as exc:
                            return StreamResult(((val, None), None), exc, _SFlow.EXCP)  # type: ignore
                        if ret in self.cache:
                            old = self.cache[ret]
                            return StreamResult(((val, old), ret))
                        self.cache[ret] = val
                        return StreamResult(((val, None), ret), None, _SFlow.SKIP)  # type: ignore
                    case _:
                        return StreamResult(((e.val, None), None), e.exc, e.flw)  # type: ignore

        self.__stack.append(w())
        return self  # type: ignore

    def call(self, func: Callable[..., _R]) -> Stream[_R]:
        def w(e: StreamResult[_T]) -> StreamResult[_R | None]:
            match e:
                case StreamResult(val, None, _SFlow.NORM):
                    try:
                        match val:
                            case [[*a], {**k}]:
                                return StreamResult(func(*a, **k))  # type: ignore
                            case [*a]:
                                return StreamResult(func(*a))
                            case {**k}:
                                return StreamResult(func(**k))
                            case a:
                                return StreamResult(func(a))
                    except Exception as exc:
                        return StreamResult(val, exc, _SFlow.EXCP)  # type: ignore
                case _:
                    return e  # type: ignore

        self.__stack.append(w)
        return self  # type: ignore

    def act(self, func: Callable[[_T], Any]) -> Stream[_T]:
        def w(e: StreamResult[_T]) -> StreamResult[_T | None]:
            match e:
                case StreamResult(val, None, _SFlow.NORM):
                    try:
                        func(val)
                        return StreamResult(val)
                    except Exception as exc:
                        return StreamResult(val, exc, _SFlow.EXCP)
                case _:
                    return e  # type: ignore
                # This error makes no sense

        self.__stack.append(w)
        return self

    def reduce(self, func: Callable[[_T, _T], _T], defaultvalue: _D = None) -> _T | _D:
        try:
            res = next(self)
        except StopIteration:
            return defaultvalue
        for val in self:
            res = func(res, val)
        return res

    @property
    def list(self) -> list[_T]:
        return list(self)

    @property
    def tuple(self) -> tuple[_T]:
        return tuple(self)

    @property
    def set(self) -> set[_T]:
        return set(self)

    @property
    def frozenset(self) -> frozenset[_T]:
        return frozenset(self)

    @property
    def null(self) -> None:
        for _ in self:
            pass

    @property
    def any(self) -> bool:
        return any(self)

    @property
    def all(self) -> bool:
        return all(self)

    @property
    def none(self) -> bool:
        return not any(self)

    @property
    def count(self) -> int:
        return sum(1 for _ in self)

    def groupby(self, func: Callable[[_T], _R]) -> dict[_R, list[_T]]:
        ret = dict[_R, list[_T]]()
        for val in self:
            r = func(val)
            if r not in ret:
                ret[r] = []
            ret[r].append(val)
        return ret

    def print(self, format: str = "") -> None:
        print("<" + ", ".join(self.eval(lambda x: x.__format__(format))) + ">")

    @property
    def stalin(self) -> Stream[_T]:
        class w:
            def __init__(self) -> None:
                self.max: _T
                self.primed = False

            def __call__(self, e: StreamResult[_T]) -> StreamResult[_T]:
                match e:
                    case StreamResult(val, None, _SFlow.NORM):
                        if not self.primed:
                            self.primed = True
                            self.max = val
                            return StreamResult(val)
                        try:
                            nmax = max(self.max, val)  # type: ignore
                        except Exception as exc:
                            return StreamResult(val, exc, _SFlow.EXCP)
                        if nmax != self.max:
                            self.max = nmax
                            return StreamResult(val)
                        return StreamResult(val, None, _SFlow.SKIP)
                    case _:
                        return e

        self.__stack.append(w())
        return self  # type: ignore


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
    def robin(*streams: Stream[_T]) -> Stream[_T]:
        __iter = zip(*(s._iter_raw_() for s in streams))
        return Stream((e for es in __iter for e in es), forceraw=True)  # type: ignore

    @staticmethod
    def robin_longest(*streams: Stream[_T]) -> Stream[_T]:
        __sent = object()
        __iter = zip_longest(*(s._iter_raw_() for s in streams), fillvalue=__sent)
        return Stream(
            (e for es in __iter for e in es if e is not __sent), forceraw=True
        )  # type: ignore

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
                        _SFlow.EXCP,
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
                        _SFlow.EXCP,
                    )
                else:
                    yield (StreamResult(tuple(t.val for t in ts)))

        return Stream(__iter(*streams), forceraw=True)  # type: ignore

    @staticmethod
    def range(*args) -> Stream[int]:
        return Stream(range(*args))

    @staticmethod
    def count(*args, **kwargs) -> Stream[int]:
        return Stream(count(*args, **kwargs))

    @staticmethod
    def randint(a: int, b: int) -> Stream[int]:
        return Stream((randint(a, b) for _ in count()))


def null(__iter: Iterable[Any]) -> None:
    for _ in __iter:
        ...
