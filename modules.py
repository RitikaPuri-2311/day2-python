# =============================================================================
# TOPIC: Modules & Packages
# Covers: import styles, __name__=='__main__', packages, relative imports,
#         sys.path, how Python finds modules
# =============================================================================



# a) Import the whole module — access via module.attribute
import os
import math

print(os.getcwd())          # current working directory
print(math.sqrt(16))        # 4.0

# b) Import specific names into current namespace
from os.path import join, exists, dirname

print(join("/home", "user", "docs"))   # /home/user/docs
print(exists("/tmp"))                  # True / False

# c) Import with alias — useful for long names or naming conflicts
import datetime as dt
import os.path as osp

today = dt.date.today()
print(today)
print(osp.basename("/some/path/file.py"))   # file.py

# d) Import everything (avoid in production — pollutes namespace)
# from math import *    ← generally discouraged


# -----------------------------------------------------------------------------
# 2. __name__ == '__main__' pattern
#
#    Every .py file has a __name__ attribute.
#    When run DIRECTLY:      __name__ == '__main__'
#    When IMPORTed by code:  __name__ == the module's filename (without .py)
#
#    This guard lets a file be BOTH importable AND runnable.
# -----------------------------------------------------------------------------

def compute_circle_area(radius: float) -> float:
    """Return area of a circle."""
    return math.pi * radius ** 2

def compute_circumference(radius: float) -> float:
    """Return circumference of a circle."""
    return 2 * math.pi * radius

if __name__ == "__main__":
    # This block only runs when you do:  python modules.py
    # It does NOT run when another file does:  import modules
    r = 5
    print(f"Circle r={r}: area={compute_circle_area(r):.2f}, circ={compute_circumference(r):.2f}")


# -----------------------------------------------------------------------------
# 3. How Python Finds Modules — sys.path
#
#    When you write `import foo`, Python searches directories in sys.path:
#      [0] '' or the script's directory
#      [1] PYTHONPATH environment variable entries
#      [2] Installation-dependent default (site-packages, stdlib)
# -----------------------------------------------------------------------------

import sys

print("\n--- sys.path ---")
for p in sys.path:
    print(" ", p or "(current directory)")

# You can add paths at runtime (useful for monorepos / scripts):
# sys.path.insert(0, "/path/to/my/libraries")

# importlib — inspect modules programmatically
import importlib

spec = importlib.util.find_spec("json")
print(f"\njson module location: {spec.origin}")   # shows path to json.py




print("\nmodules.py loaded successfully.")