from abc import ABC, abstractmethod
from typing import Callable, Collection, Iterable, Mapping, Self, TypeVar

_K = TypeVar("_K")
_V = TypeVar("_V")


class AbstractBag(ABC, Mapping[_K, _V]):
    def __init__(self) -> None:
        self._data: dict[_K, Collection[_V]] = {}

    @abstractmethod
    def append(self, key: _K, val: _V) -> None:
        ...

    def extend(self, iter: Iterable[tuple[_K, _V]]):
        for k, v in iter:
            self.append(k, v)

    def join(self, other: Self):
        self.extend(other.items())

    def __repr__(self):
        return f"{self.__class__.__name__}({self._data.__repr__()})"

    def __contains__(self, elm: _V):
        return any(elm in vs for vs in self._data.values())

    def keys(self) -> Iterable[_K]:
        yield from self._data.keys()

    def items(self) -> Iterable[tuple[_K, _V]]:
        yield from ((k, v) for k, vs in self._data.items() for v in vs)

    def elements(self) -> Iterable[_V]:
        yield from (v for _, v in self.items())

    def __iter__(self) -> Iterable[_K]:
        yield from self.keys()

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, __key: _K) -> Collection[_V]:
        return self._data.__getitem__(__key)


class Bag(AbstractBag, Mapping[_K, _V]):
    def __init__(self) -> None:
        super().__init__()
        self._data: dict[_K, list[_V]]

    def append(self, key: _K, val: _V) -> None:
        if key not in self._data:
            self._data[key] = []
        self._data[key].append(val)

    def __getitem__(self, __key: _K) -> tuple[_V]:
        if __key in self._data:
            return tuple(self._data[__key])
        return tuple()


class Pouch(Bag, Mapping[_K, _V]):
    def __init__(self, key: Callable[[_V], _K]) -> None:
        super().__init__()
        self.__key = key

    def add(self, val: _V):
        self.append(self.__key(val), val)

    def adds(self, iter: Iterable[_V]):
        for v in iter:
            self.add(v)


class Sack(AbstractBag, Mapping[_K, _V]):
    def __init__(self) -> None:
        super().__init__()
        self._data: dict[_K, set[_V]]

    def append(self, key: _K, val: _V) -> None:
        if key not in self._data:
            self._data[key] = set()
        self._data[key].add(val)

    def __getitem__(self, __key: _K) -> frozenset[_V]:
        if __key in self._data:
            return frozenset(self._data[__key])
        return frozenset()


class Stash(Sack, Mapping[_K, _V]):
    def __init__(self, key: Callable[[_V], _K]) -> None:
        super().__init__()
        self.__key = key

    def add(self, val: _V):
        self.append(self.__key(val), val)

    def adds(self, iter: Iterable[_V]):
        for v in iter:
            self.add(v)
