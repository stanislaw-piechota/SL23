"""
This is the main program file
"""
import fib
from time import time


def compare_times(n):
    """
    Function prints runtime of
    different methods to calculate
    n-th number of Fibonacci series.

    Function is void type
    """
    print("Iteration method:")
    i_start_time = time()
    print(fib.fib(n))
    print(f"Runtime [s] = {time()-i_start_time}")
    
    r_start_time = time()
    fib.fib_r(n)
    print(f"Runtime [s] = {time()-r_start_time}")


if __name__ == "__main__":
    print("Using functions from fib library and time comparison:")
    compare_times(40)
    print(fib.fib_series(21))
    print(fib.fib_upto(21))
