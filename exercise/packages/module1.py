from packages.custom_exceptions import InvalidInputError


def add(a, b):
    try:
        return a + b

    except TypeError:
        raise InvalidInputError("Only numbers are allowed")


def divide(a, b):

    try:

        if b == 0:
            raise InvalidInputError("Cannot divide by zero")

        return a / b

    except TypeError:
        raise InvalidInputError("Invalid input type")


def factorial(n):

    try:

        if n < 0:
            raise InvalidInputError("Negative number not allowed")

        if n == 0 or n == 1:
            return 1

        return n * factorial(n - 1)

    except TypeError:
        raise InvalidInputError("Input must be integer")