# with statement: with open('file.txt') as f:
# Why it's better than try/finally.
#  enter and exit.
#  contextlib.contextmanager decorator.
#  Write your own context manager.

"""A context manager is an object that is notified when a context (a block of code) starts and ends."""

""" For example, file objects are context managers. When a context ends, the file object is closed automatically:"""
#  with open("random.txt") as f:
#     # data = f.read()  # returns the entire content as it is
#     # data = f.readlines()  # returns a list of lines
#     for line in f:
#         print(line.strip(), end=" ")
#         # file is closed automatically , even if an error occurs

import contextlib


@contextlib.contextmanager
def my_context(num):
    print("Entering the context")
    yield num * 2
    print("Exiting the context")


with my_context(5) as cm:
    print(f"inside the context :: {cm}")