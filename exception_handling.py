# =============================================================================
# TOPIC: Exception Handling
# Covers: try/except/else/finally, specific catches, raise, custom exceptions,
#         exception hierarchy, logging with loguru
#
# Setup:  pip install loguru
# =============================================================================

import sys

try:
    from loguru import logger
    # Configure loguru: remove default handler and add a cleaner one
    logger.remove()
    logger.add(sys.stderr, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}")
    LOGURU_AVAILABLE = True
except ImportError:
    LOGURU_AVAILABLE = False
    import logging
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)-8s | %(message)s")
    logger = logging.getLogger(__name__)
    print("[warn] loguru not installed. Run: pip install loguru")


# =============================================================================
# 1. Basic try / except / else / finally
#
#   try:        code that might raise an exception
#   except:     runs ONLY when an exception occurred
#   else:       runs ONLY when NO exception occurred  ← often forgotten!
#   finally:    ALWAYS runs (cleanup — close files, release locks, etc.)
# =============================================================================

def safe_divide(a: float, b: float) -> float | None:
    try:
        result = a / b                  # might raise ZeroDivisionError
    except ZeroDivisionError:
        logger.error("Division by zero attempted: {} / {}", a, b)
        return None
    else:
        # Only reached if no exception was raised
        logger.success("Division succeeded: {} / {} = {}", a, b, result)
        return result
    finally:
        # Always runs — good place for cleanup
        logger.debug("safe_divide({}, {}) finished", a, b)

print(safe_divide(10, 2))    # 5.0
print(safe_divide(10, 0))    # None


# =============================================================================
# 2. Catching Specific Exceptions
#
#   Always catch the MOST SPECIFIC exception you can.
#   Bare `except:` or `except Exception:` hides bugs.
# =============================================================================

def parse_user_age(raw: str) -> int:
    try:
        age = int(raw)                  # ValueError if not a number
        if age < 0 or age > 150:
            raise ValueError(f"Age {age} is out of realistic range")
        return age
    except ValueError as e:
        logger.warning("Invalid age input '{}': {}", raw, e)
        return -1

print(parse_user_age("25"))      # 25
print(parse_user_age("abc"))     # -1
print(parse_user_age("-5"))      # -1


# Catching MULTIPLE exception types in one except clause
def read_config_value(data: dict, key: str, index: int = 0):
    try:
        return data[key][index]
    except (KeyError, IndexError, TypeError) as e:
        logger.error("Config read failed — {}: {}", type(e).__name__, e)
        return None

cfg = {"ports": [8000, 8001]}
print(read_config_value(cfg, "ports", 0))   # 8000
print(read_config_value(cfg, "missing", 0)) # None (KeyError caught)
print(read_config_value(cfg, "ports", 9))   # None (IndexError caught)


# =============================================================================
# 3. raise — explicitly raise exceptions
#
#   raise SomeException("message")       ← raise a new exception
#   raise                                ← re-raise the current exception
# =============================================================================

def validate_email(email: str) -> str:
    if "@" not in email:
        raise ValueError(f"'{email}' is not a valid email address")
    if len(email) > 254:
        raise ValueError("Email address exceeds maximum length of 254 chars")
    return email.lower().strip()

try:
    print(validate_email("user@example.com"))   # ok
    print(validate_email("not-an-email"))       # raises
except ValueError as e:
    logger.error("Validation error: {}", e)


# Re-raise after logging
def load_file(path: str) -> str:
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError as e:
        logger.critical("Cannot find required file: {}", path)
        raise   # re-raise the original exception unchanged


# =============================================================================
# 4. Custom Exception Classes
#
#   Inherit from Exception (or a more specific built-in).
#   Add attributes to carry extra context.
# =============================================================================

class AppError(Exception):
    """Base class for all application-specific errors."""
    pass

class ConfigurationError(AppError):
    """Raised when the app is misconfigured."""
    def __init__(self, key: str, message: str = ""):
        self.key = key
        super().__init__(message or f"Missing or invalid config key: '{key}'")

class DatabaseError(AppError):
    """Raised when a database operation fails."""
    def __init__(self, operation: str, detail: str = ""):
        self.operation = operation
        super().__init__(f"DB error during '{operation}': {detail}")

class NotFoundError(AppError):
    """Raised when a requested resource doesn't exist."""
    def __init__(self, resource: str, identifier):
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} with id={identifier!r} not found")


# Using custom exceptions
def get_user(user_id: int) -> dict:
    fake_db = {1: {"name": "Alice"}, 2: {"name": "Bob"}}
    if user_id not in fake_db:
        raise NotFoundError("User", user_id)
    return fake_db[user_id]

try:
    user = get_user(99)
except NotFoundError as e:
    logger.warning("{}", e)
    print(f"Resource: {e.resource}, ID: {e.identifier}")


# =============================================================================
# 5. Exception Hierarchy (Python built-ins, simplified)

# Catching at different levels
def demonstrate_hierarchy():
    try:
        raise DatabaseError("SELECT", "connection refused")
    except NotFoundError:
        print("not found")          # NOT reached
    except DatabaseError as e:
        print(f"DB error: {e}")     # ← reached first (most specific)
    except AppError:
        print("app error")          # would also catch DatabaseError
    except Exception:
        print("any exception")      # widest net


demonstrate_hierarchy()


# =============================================================================
# 6. Logging with loguru
#
#   Loguru replaces Python's standard logging with a simpler API.
#   Levels: TRACE < DEBUG < INFO < SUCCESS < WARNING < ERROR < CRITICAL
# =============================================================================

if LOGURU_AVAILABLE:
    # Add a file sink for persistent logs
    logger.add(
        "app.log",
        rotation="10 MB",       # new file after 10 MB
        retention="7 days",     # delete logs older than 7 days
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} — {message}"
    )

    logger.trace("Very verbose trace message")
    logger.debug("Debug: variable x = {}", 42)
    logger.info("Application started on port {}", 8000)
    logger.success("User {} logged in successfully", "alice@example.com")
    logger.warning("Disk usage above {}%", 80)
    logger.error("Failed to connect to database")
    logger.critical("Unrecoverable state — shutting down")

    # Catching + logging exceptions with traceback
    def risky():
        return 1 / 0

    try:
        risky()
    except ZeroDivisionError:
        logger.exception("Caught an exception (traceback included above):")


print("\nexception_handling.py complete.")