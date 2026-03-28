# AGENTS.md — fitbit-cli

This file provides guidance for agentic coding agents working in this repository.

---

## Project Overview

`fitbit-cli` is a Python CLI tool for fetching and displaying personal health data from the Fitbit API. It uses OAuth2 PKCE for authentication, the `requests` library for HTTP calls, and `rich` for terminal output.

- **Language:** Python 3.10+
- **Entry point:** `fitbit_cli/main.py` → `main()`
- **CLI installed as:** `fitbit-cli`
- **Token storage:** `~/.fitbit/token.json`

---

## Repository Layout

```
fitbit_cli/
  __init__.py       # Package version (__version__ = "1.5.2")
  cli.py            # argparse setup; date parsing utilities
  exceptions.py     # FitbitInitError, FitbitAPIError
  fitbit_api.py     # FitbitAPI class wrapping all Fitbit REST endpoints
  fitbit_setup.py   # OAuth2 PKCE flow; token read/write/update
  formatter.py      # rich-based display functions; CONSOLE singleton
  main.py           # Entrypoint: wires CLI args → API calls → formatters
tests/
  cli_test.py       # unittest-based tests for date parsing logic
pyproject.toml      # Build system + tool configuration (black, isort, pylint, mypy)
setup.py            # Package metadata and runtime dependencies
```

---

## Environment Setup

```bash
git clone git@github.com:veerendra2/fitbit-cli.git
cd fitbit-cli
python -m venv venv
source venv/bin/activate
pip install -e .
# Install dev/lint tools
pip install black isort pylint mypy pytest pytest-cov
```

---

## Build & Install

```bash
# Editable install (development)
pip install -e .

# Build distribution
pip install build
python -m build
```

---

## Running Tests

### Run all tests

```bash
pytest tests/
```

### Run all tests with coverage

```bash
pytest tests/ --cov=fitbit_cli
```

### Run a single test file

```bash
pytest tests/cli_test.py
```

### Run a single test case by name

```bash
pytest tests/cli_test.py::TestCLIDateFunctions::test_get_date_range
```

### Run tests using unittest directly

```bash
python -m unittest discover -s tests -p "*_test.py"
# or a specific test:
python -m unittest tests.cli_test.TestCLIDateFunctions.test_get_date_range
```

**Test file naming convention:** `*_test.py` (not `test_*.py`).

---

## Linting & Formatting

All tools are configured in `pyproject.toml`.

### Format code with black

```bash
black fitbit_cli/ tests/
```

### Sort imports with isort

```bash
isort fitbit_cli/ tests/
```

### Lint with pylint

```bash
pylint fitbit_cli/
```

### Type-check with mypy

```bash
mypy fitbit_cli/
```

### Run all checks (matches CI)

```bash
black --check fitbit_cli/ tests/
isort --check-only fitbit_cli/ tests/
pylint fitbit_cli/
mypy fitbit_cli/
pytest tests/ --cov=fitbit_cli
```

**Tool settings:**
- `black`: `line-length = 88`
- `isort`: `profile = "black"` (compatible with black)
- `pylint`: `max-line-length = 120`; `E0401` (import errors) disabled globally
- `mypy`: `ignore_missing_imports = true`
- `flake8` and `ruff` are **not used** in this project

---

## Code Style Guidelines

### File Header

Every source file begins with an encoding declaration and a module docstring:

```python
# -*- coding: utf-8 -*-
"""
Module Description
"""
```

### Imports

- Order: stdlib → third-party (`requests`, `rich`) → relative (`. import ...`)
- Managed by `isort` with `profile = "black"`
- Relative imports are used within the package:

```python
from .exceptions import FitbitAPIError
from .fitbit_setup import update_fitbit_token
```

- Use `from . import module as alias` for module-level imports:

```python
from . import fitbit_setup as setup
from . import formatter as fmt
```

### Naming Conventions

| Kind | Convention | Example |
|------|------------|---------|
| Classes | `PascalCase` | `FitbitAPI`, `FitbitInitError` |
| Functions / methods | `snake_case` | `get_sleep_log`, `parse_date_range` |
| Private helpers | `_leading_underscore` | `_create_headers`, `_get_date_range` |
| Module-level constants | `UPPER_SNAKE_CASE` | `BASE_URL`, `TOKEN_URL`, `CONSOLE` |
| Variables | `snake_case` | `start_date`, `access_token` |

### Docstrings

- All public classes, methods, and functions must have a one-line docstring.
- Format: `"""Short imperative description."""` — no blank line after the `def`.

```python
def get_sleep_log(self, start_date, end_date=None):
    """Get Sleep Logs by Date Range and Date"""
    ...
```

### Type Annotations

Type annotations are **not currently used** in source files. `mypy` is configured but set to `ignore_missing_imports = true`. Do not add annotations unless refactoring a file end-to-end for consistency.

### String Formatting

Use **f-strings** throughout. Do not use `%`-formatting or `.format()`.

```python
url = f"https://api.fitbit.com/1/user/-/sleep/date/{date_range}.json"
raise FitbitAPIError(f"HTTP error occurred: {response.json()}")
```

### Error Handling

- Custom exceptions live in `fitbit_cli/exceptions.py`.
- Both exception classes accept a single `message` arg and store it as `self.message`.
- Use specific exception types; avoid bare `except:` clauses.
- Preserve tracebacks with `raise ... from e`.
- HTTP 401 responses trigger an automatic token refresh inside `make_request()`.

```python
class FitbitAPIError(Exception):
    """Custom exception for Fitbit API"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message
```

```python
except requests.exceptions.HTTPError as e:
    if response.status_code == 401:
        self.refresh_access_token()
        ...
    else:
        raise FitbitAPIError(f"HTTP error occurred: {response.json()}") from e
```

### HTTP Requests

All `requests` calls must include `timeout=5`:

```python
response = requests.request(method, url, headers=self.headers, timeout=5, **kwargs)
```

### Rich Output

All terminal output goes through `formatter.py`. The `CONSOLE` singleton is a module-level constant:

```python
CONSOLE = Console()
```

Never print directly; use `CONSOLE.print(...)` or the `rich` table APIs.

### pylint Inline Suppression

Use inline directives sparingly and only when justified:

```python
# pylint: disable=C0301   # line too long
# pylint: disable=C0413   # import not at top (test files adding sys.path)
# pylint: disable=C0103   # invalid variable name
```

---

## Testing Conventions

- Framework: `unittest.TestCase` (tests are structured as unittest, run by pytest).
- Test files named `*_test.py` and placed in `tests/`.
- One test class per file, named `Test<Subject>`.
- Each test method has a full docstring describing what it verifies.
- Use `unittest.mock.patch` to mock `datetime.today()` for deterministic date tests.
- Add `sys.path.insert(0, ...)` at the top of test files when needed to resolve imports.

---

## CI/CD

Defined in `.github/workflows/`:

- **ci.yml**: Runs on PRs. Executes `super-linter` (black + isort + pylint; flake8/ruff disabled) then `pytest --cov` on Python 3.12.
- **release.yml**: Triggered on GitHub Release creation. Publishes to PyPI via `twine`.
- **dependabot.yml**: Weekly updates for `pip` and `github-actions` dependencies.

---

## Runtime Notes

- OAuth2 PKCE setup runs a temporary local server on `127.0.0.1:8080` to receive the auth code.
- Token file: `~/.fitbit/token.json` — contains `client_id`, `secret`, `access_token`, `refresh_token`.
- Tokens are valid for 8 hours and auto-refreshed on 401 responses.
- Only GET endpoints are implemented in `FitbitAPI`.
