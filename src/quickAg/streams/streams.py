from __future__ import annotations

from enum import Enum
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Iterator,
    Literal,
    NamedTuple,
    TypeVar,
)
from itertools import count, zip_longest
from random import random, randint


class _SFlow(Enum):
    NORM = 0
    SKIP = 1
    STOP = 2
    STAF = 3


_T = TypeVar("_T")
_R = TypeVar("_R")


class StreamResult(NamedTuple, Generic[_T]):
    val: _T
    exc: Exception | None
    flw: _SFlow


class Stream(Iterator[_T], Generic[_T]):
    def __init__(self, __iter: Iterable[_T]):
        if not isinstance(__iter, Iterator):
            self.__iter = iter(__iter)
        else:
            self.__iter = __iter
        self.__stack: list[Callable[[StreamResult], StreamResult]] = []
        self.__status: _SFlow = _SFlow.NORM

    def __iter__(self) -> Iterator[_T]:
        return self

    def __next__(self) -> _T:
        if self.__status == _SFlow.STOP:
            raise StopIteration

        e = StreamResult(self.__iter.__next__(), None, _SFlow.NORM)

        for ev in self.__stack:
            e = ev(e)
            match e.flw:
                case _SFlow.NORM:
                    continue
                case _SFlow.SKIP:
                    return self.__next__()
                case _SFlow.STOP:
                    raise StopIteration
                case _SFlow.STAF:
                    self.__status = _SFlow.STOP

        if e.exc is not None:
            raise e.exc
        return e.val

    def filter(self, key: Callable[[_T], bool]) -> Stream[_T]:
        def w(e: StreamResult[_T]):
            if e.exc is not None: return e
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
            if e.exc is not None: return e
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
            if e.exc is not None: return e
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
            if e.exc is not None: return e
            try:
                return StreamResult(
                    e.val, None, _SFlow.STAF if key(e.val) else _SFlow.NORM
                )
            except Exception as exc:
                return StreamResult(e.val, exc, _SFlow.NORM)

        self.__stack.append(w)
        return self

    def eval(self, func: Callable[[_T], _R]) -> Stream[_R]:
        def w(e: StreamResult[_T]) -> StreamResult[_R | None]:
            if e.exc is not None: return e # type: ignore
            try:
                return StreamResult(func(e.val), None, _SFlow.NORM)
            except Exception as exc:
                return StreamResult(None, exc, _SFlow.NORM)

        self.__stack.append(w)
        return self  # type: ignore

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

    @property
    def unique(self):
        cache = set[_T]()

        def w(e: StreamResult[_T]) -> StreamResult[_T]:
            if e.exc is not None: return e
            if e.val in cache:
                return StreamResult(e.val, None, _SFlow.SKIP)
            cache.add(e.val)
            return StreamResult(e.val, None, _SFlow.NORM)

        self.__stack.append(w)
        return self


class callproperty(property):
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self.fget is not None:
            return self.fget(*args, **kwds)


class streammeta(type):
    @property
    def naturals(self) -> Stream[int]:
        return Stream(count())

    @property
    def integers(self) -> Stream[int]:
        return stream.robin(Stream(count(0, -1)), Stream(count(1, 1)))

    @property
    def rand(self) -> Stream[float]:
        return Stream((random() for _ in count()))

    random = rand


class stream(metaclass=streammeta):
    def __new__(cls, __iter: Iterable[_T]) -> Stream[_T]:
        return Stream(__iter)

    @staticmethod
    def robin(*streams: Stream[_T]) -> Stream[_T]:
        return Stream(e for es in zip(*streams) for e in es)

    @staticmethod
    def zip(*streams: Stream[_T]) -> Stream[tuple[_T, ...]]:
        return Stream(es for es in zip(*streams))

    @staticmethod
    def zip_longest(
        *streams: Stream[_T], fillvalue: Any = None
    ) -> Stream[tuple[_T, ...]]:
        return Stream(es for es in zip_longest(*streams, fillvalue=fillvalue))

    @staticmethod
    def range(*args):
        return Stream(range(*args))

    @staticmethod
    def count(*args):
        return Stream(count(*args))
