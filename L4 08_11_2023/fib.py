"""
Fuctions related to Fibonacci squence.

The module provides functions returning
numbers from Fibonacci sequnce
as single values or lists.
"""


def fib(n):
    """
    Return n-th number
    of the Fibonacci series
    using iteration.

    For n<=0, function returns 0
    """
    if n <= 0:
        return 0
    a, b = 0, 1
    for i in range(n-1):
        a, b = b, a+b
    return b


def fib_r(n):
    """
    Return n-th number
    of the Fibonacci series
    using recursion.

    For n<=0, function returns 0
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fib_r(n-1) + fib_r(n-2)


def fib_series(n):
    """
    Return the list of n-numbers
    from Fibonacci series.

    For n<=0, function returns []
    """
    series = []
    if n <= 0:
        return series
    a, b = 0, 1
    for i in range(n):
        series.append(a)
        a, b = b, a+b
    return series


def fib_upto(n):
    """
    Return the list of all Fibonacci
    numbers lower than n.

    For n<=0, function returns []
    """
    series = []
    a, b = 0, 1
    while a < n:
        series.append(a)
        a, b = b, a+b
    return series


if __name__ == "__main__":
    print("Library tests:")
    print(fib(50))
    print(fib_r(32))
    print(fib_series(10))
    print(fib_upto(100))
