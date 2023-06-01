import queue
import threading
from collections.abc import Callable, Iterable, Mapping
from typing import Any, Generic, TypeVar
from sys import stderr

_T = TypeVar("_T")
_R = TypeVar("_R")
_S = TypeVar("_S")


class rThread(threading.Thread, Generic[_R]):
    """This class is a subclass of threading.Thread and allows the handling of
    threads with return values and exceptions. It does so via the added properties
    result and exception. It also implements the method fuse() that operates
    similarly to join() and returns the return value of the target function."""

    def __init__(
        self,
        group: None = None,
        target: Callable[..., _R] | None = None,
        name: str | None = None,
        args: Iterable[Any] = ...,
        kwargs: Mapping[str, Any] | None = None,
        *,
        daemon: bool | None = None
    ) -> None:
        """This constructor should always be called with keyword arguments. Arguments are:

        *group* should be None; reserved for future extension when a ThreadGroup
        class is implemented.

        *target* is the callable object to be invoked by the run()
        method. Defaults to None, meaning nothing is called.

        *name* is the thread name. By default, a unique name is constructed of
        the form "Thread-N" where N is a small decimal number.

        *args* is a list or tuple of arguments for the target invocation. Defaults to ().

        *kwargs* is a dictionary of keyword arguments for the target
        invocation. Defaults to {}.

        If a subclass overrides the constructor, it must make sure to invoke
        the base class constructor (Thread.__init__()) before doing anything
        else to the thread.

        """
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._ret: _R
        self._exc: Exception | None = None

    def run(self):
        """Method representing the thread's activity.

        You may override this method in a subclass. The standard run() method
        invokes the callable object passed to the object's constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the args and kwargs arguments, respectively.

        """
        try:
            if self._target is not None:  # type: ignore
                try:
                    self._ret = self._target(*self._args, **self._kwargs)  # type: ignore
                except Exception as e:
                    self._exc = e
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs  # type: ignore

    @property
    def result(self) -> _R:
        """The property represents the return value of the target function. If
        the thread is still alive then a ValueError is raised, and if the thread
        raised an exception then the traceback is printed to stderr and a
        RuntimeError is raised."""
        if self.is_alive():
            raise ValueError("The thread is still running and has no return value")
        if self._exc is not None:
            print(self._exc.__traceback__, file=stderr)
            raise RuntimeError(
                "The thread has no return value as an exception happened"
            )
        return self._ret

    @property
    def exception(self) -> Exception | None:
        """The property represents the uncaught exception that stopped the thread.
        If the thread is still alive then a ValueError is raised. If no exception
        was raised in the thread then this will return None."""
        if self.is_alive():
            raise ValueError(
                "The thread is still running and cannot have raised exceptions"
            )
        return self._exc

    def fuse(self, timeout: float | None = None) -> _R | None:
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


class qThread(threading.Thread, Generic[_T, _R]):
    """This class is a subclass of threading.Thread and facilitates the creation
    of threads with a double queue to transmit messages to the main thread.
    The target function must allow for *queueTX* and *queueRX* keyword arguments,
    that represent the two queues (transmit and receive).
    In order to communicate with the thread from the main thread the functions
    put() and get() are to be used."""

    def __init__(
        self,
        group: None = None,
        target: Callable[..., Any] | None = None,
        name: str | None = None,
        args: Iterable[Any] = ...,
        kwargs: Mapping[str, Any] | None = None,
        *,
        daemon: bool | None = None
    ) -> None:
        """This constructor should always be called with keyword arguments. Arguments are:

        *group* should be None; reserved for future extension when a ThreadGroup
        class is implemented.

        *target* is the callable object to be invoked by the run()
        method. Defaults to None, meaning nothing is called.

        *name* is the thread name. By default, a unique name is constructed of
        the form "Thread-N" where N is a small decimal number.

        *args* is a list or tuple of arguments for the target invocation. Defaults to ().

        *kwargs* is a dictionary of keyword arguments for the target
        invocation. Defaults to {}.

        If a subclass overrides the constructor, it must make sure to invoke
        the base class constructor (Thread.__init__()) before doing anything
        else to the thread.

        """
        self._queueTX = queue.Queue[_T]()
        self._queueRX = queue.Queue[_R]()

        if target is None:
            super().__init__(group, target, name, args, kwargs, daemon=daemon)
        else:

            def _target(*args, **kwargs):
                return target(
                    *args, queueRX=self._queueTX, queueTX=self._queueRX, **kwargs
                )

            super().__init__(group, _target, name, args, kwargs, daemon=daemon)

    def put(self, _val: _T, block: bool = True, timeout: float | None = None) -> None:
        """The function puts an object onto the RX queue of the thread. The
        syntax is identical to queue.Queue.put()"""
        self._queueTX.put(_val, block=block, timeout=timeout)

    def get(self, block: bool = True, timeout: float | None = None) -> _R:
        """The function gets an object from the TX queue of the thread. The
        syntax is identical to queue.Queue.get()"""
        return self._queueRX.get(block=block, timeout=timeout)


# TODO: in pyi make that if defaultstatus is not given then _S is Any
class sThread(rThread, threading.Thread, Generic[_R, _S]):
    """This class is a subclass of threading.Thread and creates threads with a
    status variable, exposed to the thread via the setstatus() function.
    The target function must allow for *setstatus()* as a  keyword argument.
    The status can be checked via the status property. The status is protected by
    a threading.Lock object, so both status and setstatus() might become expensive
    operations if done frequently.

    It is possible to read without the lock by using the function status_nowait()
    and to write the status by calling setstatus() with the keyword argument block
    set to false.
    Doing so might result in race conditions between the two threads."""

    def __init__(
        self,
        group: None = None,
        target: Callable[..., _R] | None = None,
        name: str | None = None,
        args: Iterable[Any] = ...,
        kwargs: Mapping[str, Any] | None = None,
        defaultstatus: _S = None,
        *,
        daemon: bool | None = None
    ) -> None:
        """This constructor should always be called with keyword arguments. Arguments are:

        *group* should be None; reserved for future extension when a ThreadGroup
        class is implemented.

        *target* is the callable object to be invoked by the run()
        method. Defaults to None, meaning nothing is called.

        *name* is the thread name. By default, a unique name is constructed of
        the form "Thread-N" where N is a small decimal number.

        *args* is a list or tuple of arguments for the target invocation. Defaults to ().

        *kwargs* is a dictionary of keyword arguments for the target
        invocation. Defaults to {}.

        *defaultstatus* is any object that represents the initial status of the
        thread. Default is None

        If a subclass overrides the constructor, it must make sure to invoke
        the base class constructor (Thread.__init__()) before doing anything
        else to the thread.

        """
        self._statuslock = threading.Lock()
        self._sts = defaultstatus

        def setstatus(_v: _S, block: bool = True) -> None:
            if block:
                with self._statuslock:
                    self._sts = _v
            else:
                self._sts = _v

        if target is None:
            super().__init__(group, target, name, args, kwargs, daemon=daemon)
        else:

            def _target(*args, **kwargs):
                return target(*args, setstatus=setstatus, **kwargs)

            super().__init__(group, _target, name, args, kwargs, daemon=daemon)

    @property
    def status(self) -> _S:
        """Returns the status of the thread. It uses threading.Lock only if the
        thread is still running."""
        if not self.is_alive():
            return self._sts

        with self._statuslock:
            return self._sts

    @property
    def status_nowait(self) -> _S:
        """Returns the status of the thread without using threading.Lock. Doing
        so might result in race conditions."""
        return self._sts
