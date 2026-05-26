# =============================================================================
# TOPIC: Functions
# Covers: *args, **kwargs, keyword-only, positional-only, decorators,
#         functools.wraps, lambda, recursion
# =============================================================================

import functools
import time



# 1. *args — Variable Positional Arguments
#    *args collects extra positional arguments into a TUPLE

def add_all(*args):
    """Sum any number of arguments."""
    # args is a tuple: (1, 2, 3) etc.
    return sum(args)

print(add_all(1, 2, 3))          # 6
print(add_all(10, 20))            # 30
print(add_all(*[5, 6, 7]))        # 18  — unpacking a list with *



# 2. **kwargs — Variable Keyword Arguments
#    **kwargs collects extra keyword arguments into a DICT

def describe_person(**kwargs):
    """Print all keyword info about a person."""
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

describe_person(name="Alice", age=30, city="Delhi")

# Combining *args and **kwargs
def mixed(a, b, *args, **kwargs):
    print(f"a={a}, b={b}, extras={args}, options={kwargs}")

mixed(1, 2, 3, 4, color="red", size=10)
# a=1, b=2, extras=(3, 4), options={'color': 'red', 'size': 10}



# 3. Keyword-Only Arguments  (defined AFTER the bare *)
#    Must be passed by name, cannot be positional

def create_user(name, *, role="viewer", active=True):
    #              ^ bare * forces everything after it to be keyword-only
    return {"name": name, "role": role, "active": active}

print(create_user("Bob"))                          # uses defaults
print(create_user("Carol", role="admin"))          # keyword arg
# create_user("Dan", "editor")  ← TypeError! must use keyword



# 4. Positional-Only Arguments  (defined BEFORE the /)
#    Must be passed positionally; cannot use their names as keywords

def power(base, exp, /):
    #               ^ / forces everything before it to be positional-only
    return base ** exp

print(power(2, 10))          # 1024  ✓
# power(base=2, exp=10)      ← TypeError! positional-only

# Mix: positional-only / normal * keyword-only
def full_example(pos_only, /, normal, *, kw_only):
    return pos_only + normal + kw_only

print(full_example(1, 2, kw_only=3))   # 6



# 5. Decorators — @ syntax
#    A decorator is a function that takes a function and returns a new function.
#    Pattern:  decorated = decorator(original)
#    Sugar:    @decorator above the def

def timer(func):
    """Decorator that prints how long a function takes."""
    @functools.wraps(func)   # ← preserves __name__, __doc__ of the original
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)       # call original
        elapsed = time.perf_counter() - start
        print(f"[timer] {func.__name__} took {elapsed:.6f}s")
        return result
    return wrapper

@timer
def slow_square(n):
    """Return n squared after a tiny sleep."""
    time.sleep(0.01)
    return n * n

print(slow_square(7))          # prints timing, then 49

# Without functools.wraps the name would be "wrapper" not "slow_square"
print(slow_square.__name__)    # slow_square  ✓


# Decorator with arguments — needs an extra layer
def repeat(times):
    """Decorator factory: repeat function call `times` times."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    print(f"Hello, {name}!")

greet("World")   # prints 3 times



# 6. Lambda Functions
#    Anonymous single-expression functions: lambda params: expression
#    Good for: short callbacks, sorting keys — NOT for complex logic


square = lambda x: x ** 2
print(square(5))            # 25

# Common use: sorting key
people = [{"name": "Zara", "age": 25}, {"name": "Ali", "age": 30}, {"name": "Ben", "age": 20}]
sorted_people = sorted(people, key=lambda p: p["age"])
print([p["name"] for p in sorted_people])   # ['Ben', 'Zara', 'Ali']

# map / filter with lambda
nums = [1, 2, 3, 4, 5, 6]
evens   = list(filter(lambda x: x % 2 == 0, nums))   # [2, 4, 6]
doubled = list(map(lambda x: x * 2, nums))            # [2, 4, 6, 8, 10, 12]
print(evens, doubled)



#    A function that calls itself. MUST have a base case to stop.
#    Python default recursion limit: sys.getrecursionlimit() == 1000

def factorial(n: int) -> int:
    """
    n! = n * (n-1) * ... * 1
    Base case:  factorial(0) = 1
    Recursive:  factorial(n) = n * factorial(n-1)
    """
    if n < 0:
        raise ValueError("factorial undefined for negative numbers")
    if n == 0:          # ← BASE CASE — stops the recursion
        return 1
    return n * factorial(n - 1)   # ← RECURSIVE CASE

print(factorial(5))    # 120
print(factorial(0))    # 1


def fibonacci(n: int) -> int:
    """
    fib(0)=0, fib(1)=1, fib(n) = fib(n-1) + fib(n-2)
    Note: naive recursion is O(2^n) — use memoisation for large n.
    """
    if n <= 1:          # base cases
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print([fibonacci(i) for i in range(10)])  # [0,1,1,2,3,5,8,13,21,34]


