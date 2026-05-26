# =============================================================================
# TOPIC: pip & Virtual Environments
# Covers: pip commands, requirements.txt, venv lifecycle, why isolation matters
#
#  This file is DOCUMENTATION + runnable checks.
#  The shell commands are shown in comments — run them in your terminal.
# =============================================================================

import subprocess
import sys
import os

# -----------------------------------------------------------------------------
# 1. pip — Python's package installer
#
#    pip is installed automatically with Python 3.4+.
#    Always use:  python -m pip  (ensures you use pip for THIS interpreter)
# -----------------------------------------------------------------------------

# ── Common pip commands ──
#
#   Install a package:
#       python -m pip install requests
#
#   Install a specific version:
#       python -m pip install requests==2.31.0
#
#   Install minimum version:
#       python -m pip install "requests>=2.28"
#
#   Upgrade a package:
#       python -m pip install --upgrade requests
#
#   Uninstall:
#       python -m pip uninstall requests
#
#   List installed packages:
#       python -m pip list
#
#   Show details of one package:
#       python -m pip show requests
#
#   Search (deprecated on PyPI, use https://pypi.org instead):
#       python -m pip search requests
# ─────────────────────────────────────────────────────────────────────────────


# -----------------------------------------------------------------------------
# 2. requirements.txt — reproducible installs
#
#   Snapshot current environment:
#       python -m pip freeze > requirements.txt
#
#   Install from snapshot (on a new machine / CI):
#       python -m pip install -r requirements.txt
#
#   Example requirements.txt:
#       loguru==0.7.2
#       python-dotenv==1.0.1
#       requests==2.31.0
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# 3. Virtual Environments (venv)
#
#   A venv is an ISOLATED Python installation for one project.
#   It has its own:
#       • Python interpreter copy/symlink
#       • pip
#       • site-packages directory
#
#   So package versions in Project A can't break Project B.
# -----------------------------------------------------------------------------

# ── venv lifecycle ───────────────────────────────────────────────────────────
#
#   1. CREATE  (do this once per project, inside the project root):
#       python -m venv .venv
#           → creates .venv/ folder with Scripts/ (Win) or bin/ (Unix)
#
#   2. ACTIVATE  (do every time you open a new terminal for this project):
#       macOS / Linux:    source .venv/bin/activate
#       Windows CMD:      .venv\Scripts\activate.bat
#       Windows PS:       .venv\Scripts\Activate.ps1
#
#       Your prompt changes to:  (.venv) $
#       `which python` now points inside .venv/
#
#   3. WORK  — install packages, run scripts — all isolated:
#       pip install requests loguru python-dotenv
#
#   4. FREEZE  (before committing or sharing):
#       pip freeze > requirements.txt
#
#   5. DEACTIVATE  (when done with this project):
#       deactivate
#
#   6. RECREATE  (on a new machine or after cloning):
#       python -m venv .venv
#       source .venv/bin/activate
#       pip install -r requirements.txt
# ─────────────────────────────────────────────────────────────────────────────


# -----------------------------------------------------------------------------
# 4. What to commit vs what to ignore
#
#   .gitignore should contain:
#       .venv/          ← NEVER commit the venv folder (huge, OS-specific)
#       __pycache__/
#       *.pyc
#       .env            ← NEVER commit secrets
#
#   ALWAYS commit:
#       requirements.txt   ← so others can recreate the environment
#       .env.example       ← template showing which keys are needed (no values)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# 5. Programmatic check: are we inside a venv?
# -----------------------------------------------------------------------------

def in_virtual_env() -> bool:
    """Return True if Python is running inside a virtual environment."""
    return (
        hasattr(sys, "real_prefix")                        # old virtualenv
        or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)  # venv / pyvenv
    )

def show_environment_info():
    """Print useful info about the current Python environment."""
    print("=" * 50)
    print("Python Environment Info")
    print("=" * 50)
    print(f"Python version   : {sys.version}")
    print(f"Executable       : {sys.executable}")
    print(f"sys.prefix       : {sys.prefix}")
    print(f"Inside venv?     : {in_virtual_env()}")
    if in_virtual_env():
        print(f"venv prefix      : {sys.prefix}")
    print("=" * 50)

if __name__ == "__main__":
    show_environment_info()

    # List installed packages programmatically
    print("\nInstalled packages (via pip list):")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list", "--format=columns"],
        capture_output=True, text=True
    )
    print(result.stdout[:800], "...")  # truncate for readability