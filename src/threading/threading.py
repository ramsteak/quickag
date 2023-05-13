from collections.abc import Callable, Iterable, Mapping
import threading
from typing import Any, TypeVar, Generic

_R = TypeVar("_R")

class rThread(threading.Thread, Generic[_R]):
    def __init__(self, group: None = None, target: Callable[..., _R] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._ret:_R
        self._exc:Exception|None = None

    def run(self):
        """Method representing the thread's activity.

        You may override this method in a subclass. The standard run() method
        invokes the callable object passed to the object's constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the args and kwargs arguments, respectively.

        """
        try:
            if self._target is not None: # type: ignore
                try:
                    self._ret = self._target(*self._args, **self._kwargs) # type: ignore
                except Exception as e:
                    self._exc = e
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs # type: ignore

    @property
    def result(self) -> _R:
        if self.is_alive():
            raise ValueError("The thread is still running and has no return value")
        return self._ret

    @property
    def exception(self) -> Exception|None:
        return self._exc

    def fuse(self, timeout: float | None = None) -> _R|None:
        """Wait until the thread terminates and return its return value. If the
        thread raises an exception, returns None.

        This blocks the calling thread until the thread whose fuse() method is
        called terminates -- either normally or through an unhandled exception
        or until the optional timeout occurs.

        When the timeout argument is present and not None, it should be a
        floating point number specifying a timeout for the operation in seconds
        (or fractions thereof). If a timeout happens, that is if the thread has 
        not been join()ed, the function raises a TimeoutException.

        When the timeout argument is not present or None, the operation will
        block until the thread terminates.

        A thread can be fuse()ed many times.

        """
        super().join(timeout)
        if self.is_alive():
            raise TimeoutError
        return self.result

