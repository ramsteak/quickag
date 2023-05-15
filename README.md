# QuickAg
The package aims to combine every useful module, function and class I built. It 
is a collection of useful stuff, packaged into independent submodules.

## Threading
The threading module offers rThread, a subclass of threading.Thread that allows 
to get the return value of the thread and to get any exception raised by the 
thread.

To the threading.Thread class it adds the following
 - `.result` : the property that returns the return value of the thread. Raises 
 AttributeError if called before the thread finishes or if the thread raises an 
 exception
 - `.exception` : the exception raised by the thread. Is None if no exception has 
 been raised.
 - `.fuse()` : a modified join, returns the return value of the thread. If the given 
 timeout expires raises TimeoutError.

## Logging
The logging module offers getlogger, a factory function for logging.Logger that 
allows to easily build a logger with my preferred output style.

## Streams
The module allows the handling of object streams with dot notation, allowing for 
use-cases such as
```py
from quickAg.streams import elm, stream
list(stream.naturals.stop(elm > 5).eval(lambda x:x*2+x))
>>> [0, 3, 6, 9, 12, 15]
```
The stream handles exceptions during element evaluation, without stopping the 
stream
```py
from quickAg.streams import elm, stream
list(stream.range(5).eval(4 - elm).eval(1/elm).exc(ZeroDivisionError, "skip"))
>>>[0.25, 0.3333333333333333, 0.5, 1.0]
```
The last element results in a `ZeroDivisionError`, that gets caught and the element 
gets skipped.
The elm object is an object that returns a callable to perform the same operations 
performed on it, so `(elm + 5)(3)` is equivalent to `3 + 5`

## Math
The module offers the primes package, to check if a number is prime and to generate
primes. The module has the numbers up to 4001 cached, for better performance at
low values.

## Singleton
The module implements a thread-safe `Singleton` class, it also implements a 
decorator `singleton` method to make any class into a thread-safe singleton
