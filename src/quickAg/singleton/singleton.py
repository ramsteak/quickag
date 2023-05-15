import threading
from typing import Callable, Self, overload


class Singleton:
    __instances = dict[type, Self]()
    __lock = threading.Lock()

    def __new__(cls, *args, **kwargs) -> Self:
        if cls in Singleton.__instances:
            return Singleton.__instances[cls]
        with Singleton.__lock:
            if cls in Singleton.__instances:
                return Singleton.__instances[cls]
            obj = super().__new__(cls, *args, **kwargs)
            Singleton.__instances[cls] = obj
            return obj

    def __init__(self, *args, **kwargs) -> None:
        print(f"Singleton.__init__({self}, {args}, {kwargs}) -> {None}")

    def __init_subclass__(cls) -> None:
        print(f"Singleton.__init_subclass__({cls}) -> {None}")


@overload
def singleton(cls) -> object:
    ...


@overload
def singleton(*, truth: bool | None) -> Callable[[type], object]:
    ...


def singleton(cls=None, truth=None) -> object:
    if cls is not None:
        return cls()

    def cls__bool__(*args):
        if truth is True:
            return True
        if truth is False:
            return False
        raise NotImplementedError("The object has its truth defined as None")

    def wrap(cls):
        setattr(cls, "__bool__", cls__bool__)
        return cls()

    return wrap


@singleton(truth=None)
class Undefined:
    def __and__(self, other):
        if other:
            return self
        return other

    def __or__(self, other):
        if not other:
            return self
        return other
