# =============================================================================
# TOPIC: python-dotenv for Configuration
# Covers: load_dotenv, os.environ.get, never hardcode secrets, .env.example
#
# Setup:  pip install python-dotenv
# =============================================================================

import os
from pathlib import Path

# python-dotenv may not be installed in the demo environment; guard the import
try:
    from dotenv import load_dotenv, dotenv_values
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("[warn] python-dotenv not installed. Run: pip install python-dotenv")


# -----------------------------------------------------------------------------
# 1. What is a .env file?
#
#   A plain-text file in your project root holding KEY=VALUE pairs.
#   It is NEVER committed to git (add to .gitignore).
#   Each developer / server has their own copy.
#
#   Example .env:
#       DATABASE_URL=postgresql://user:pass@localhost/mydb
#       SECRET_KEY=supersecretkey123
#       DEBUG=true
#       PORT=8000
#
#   Example .env.example  (committed to git — keys, NO values):
#       DATABASE_URL=
#       SECRET_KEY=
#       DEBUG=
#       PORT=
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# 2. load_dotenv — reads the .env file and injects into os.environ
#
#   load_dotenv() looks for .env in the current directory by default.
#   Call it ONCE at the very start of your app (main.py / app.py).
# -----------------------------------------------------------------------------

def bootstrap_config():
    """
    Load environment variables from .env into os.environ.
    Safe to call even if .env doesn't exist (it's a no-op then).
    """
    if not DOTENV_AVAILABLE:
        return

    # Option A: load from default location (cwd/.env)
    load_dotenv()

    # Option B: explicit path
    # env_path = Path(__file__).parent.parent / ".env"
    # load_dotenv(dotenv_path=env_path)

    # Option C: override=True means .env values WIN over existing env vars
    # load_dotenv(override=True)


# -----------------------------------------------------------------------------
# 3. os.environ.get — read env vars safely
#
#   os.environ["KEY"]          → KeyError if missing  (use for required vars)
#   os.environ.get("KEY")      → None if missing       (use for optional vars)
#   os.environ.get("KEY", "x") → "x" if missing        (use with a default)
# -----------------------------------------------------------------------------

bootstrap_config()

# Reading config — always use .get with a sensible default for optional vars
DATABASE_URL  = os.environ.get("DATABASE_URL", "sqlite:///local.db")
SECRET_KEY    = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")
DEBUG         = os.environ.get("DEBUG", "false").lower() == "true"
PORT          = int(os.environ.get("PORT", "8000"))
APP_ENV       = os.environ.get("APP_ENV", "development")

print(f"DATABASE_URL : {DATABASE_URL}")
print(f"SECRET_KEY   : {SECRET_KEY[:6]}... (truncated)")
print(f"DEBUG        : {DEBUG}")
print(f"PORT         : {PORT}")
print(f"APP_ENV      : {APP_ENV}")


# -----------------------------------------------------------------------------
# 4. Settings class pattern — centralise all config in one place
#    Avoids scattering os.environ.get() calls throughout your codebase.
# -----------------------------------------------------------------------------

class Settings:
    """
    Single source of truth for application configuration.
    Reads from environment variables (populated by load_dotenv).
    """

    def __init__(self):
        self.database_url: str  = self._require("DATABASE_URL")
        self.secret_key: str    = self._require("SECRET_KEY")
        self.debug: bool        = os.environ.get("DEBUG", "false").lower() == "true"
        self.port: int          = int(os.environ.get("PORT", "8000"))
        self.app_env: str       = os.environ.get("APP_ENV", "development")

    @staticmethod
    def _require(key: str) -> str:
        """Return env var value; raise clearly if it's missing."""
        value = os.environ.get(key)
        if not value:
            raise EnvironmentError(
                f"Required environment variable '{key}' is not set.\n"
                f"Check your .env file or deployment configuration."
            )
        return value

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    def __repr__(self):
        return (
            f"Settings(env={self.app_env}, debug={self.debug}, "
            f"port={self.port})"
        )


# Safe to instantiate only if the required vars are available
if os.environ.get("DATABASE_URL") and os.environ.get("SECRET_KEY"):
    settings = Settings()
    print(f"\nSettings object: {settings}")
else:
    print("\n[demo] Required vars not set; Settings() skipped.")


# -----------------------------------------------------------------------------
# 5. dotenv_values — read .env without touching os.environ
#    Useful for comparing or debugging what's in the file vs what's live.
# -----------------------------------------------------------------------------

if DOTENV_AVAILABLE:
    env_path = Path(".env")
    if env_path.exists():
        file_vars = dotenv_values(env_path)
        print(f"\nKeys defined in .env: {list(file_vars.keys())}")
    else:
        print("\n[demo] No .env file found in current directory.")


# -----------------------------------------------------------------------------
# 6. NEVER do this (examples of what NOT to hardcode)
# -----------------------------------------------------------------------------

# BAD — secrets in source code
# DATABASE_URL = "postgresql://admin:Password123@prod.db.internal/mydb"
# API_KEY      = "sk-live-xK9mNpQrT..."
# SECRET_KEY   = "hardcoded-secret"

# GOOD — read from environment
# DATABASE_URL = os.environ.get("DATABASE_URL")
# API_KEY      = os.environ.get("API_KEY")
# SECRET_KEY   = os.environ.get("SECRET_KEY")


# -----------------------------------------------------------------------------
# 7. .gitignore snippet to always include
# -----------------------------------------------------------------------------
GITIGNORE_SNIPPET = """
# Secrets — NEVER commit
.env
.env.local
.env.*.local

# Commit this instead (keys, no values)
# .env.example ← do NOT ignore this one

# Virtual environment
.venv/
venv/
env/

# Python cache
__pycache__/
*.pyc
*.pyo
"""

print("\n--- Recommended .gitignore additions ---")
print(GITIGNORE_SNIPPET)