# QuickAg
The package aims to combine every useful module, function and class I built. It 
is a collection of useful stuff, packaged into independent submodules.

## Threading
The threading module offers rThread, a subclass of threading.Thread that allows 
to get the return value of the thread and to get any exception raised by the 
thread.

To the threading.Thread class it adds the following
 - `result` : the property that returns the return value of the thread. Raises 
 AttributeError if called before the thread finishes or if the thread raises an 
 exception
 - `exception` : the exception raised by the thread. Is None if no exception has 
 been raised.
 - `fuse` : a modified join, returns the return value of the thread. If the given 
 timeout expires raises TimeoutError.

## Logging
The logging module offers getlogger, a factory function for logging.Logger that 
allows to easily build a logger with my preferred output style.

## Streams
The streams module will be fledged out to handle java-like streams of object, 
with the ability to filter and evaluate and handle exceptions.
As of now only the elm class is implemented, that allows to define "symbolic-like"
math (`elm + 5` returns a callable that increments by 5 the given value)

## Math
The module offers the primes package, to check if a number is prime and to generate
primes. The module has the numbers up to 4001 cached, for better performance at
low values.
