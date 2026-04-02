# AGENTS.md — fitbit-cli

Guidance for agentic coding agents working in this repository.

---

## Project Overview

`fitbit-cli` is a Python command-line tool for fetching and displaying personal health data from the Fitbit API. It uses OAuth2 PKCE for authentication, the `requests` library for HTTP calls, and `rich` for terminal output.

- **Language:** Python 3.12+
- **Entry point:** `fitbit_cli/main.py` → `main()`
- **CLI installed as:** `fitbit-cli`
- **Token storage:** `~/.fitbit/token.json`

---

## Repository Layout

```
fitbit_cli/
  __init__.py       # Package version (__version__ = "1.6.0")
  cli.py            # argparse setup; date parsing utilities
  exceptions.py     # FitbitInitError, FitbitAPIError
  fitbit_api.py     # FitbitAPI class wrapping all Fitbit REST endpoints
  fitbit_setup.py   # OAuth2 PKCE flow; token read/write/update
  formatter.py      # rich-based display functions + JSON extraction; CONSOLE singleton
  output.py         # Output modes: table_display, json_display, raw_json_display
  main.py           # Entrypoint: wires CLI args → API calls → output mode
tests/
  cli_test.py       # unittest-based tests for date parsing logic
pyproject.toml      # Build system + tool configuration (black, isort, pylint, mypy)
setup.py            # Package metadata and runtime dependencies
```

---

## Commands

### Setup
```bash
pip install -e .
pip install black isort pylint mypy pytest pytest-cov
```

### Tests
```bash
pytest tests/                                                        # all tests
pytest tests/cli_test.py                                             # single file
pytest tests/cli_test.py::TestCLIDateFunctions::test_get_date_range  # single test
python -m unittest tests.cli_test.TestCLIDateFunctions.test_get_date_range
```

**Test file naming convention:** `*_test.py` (not `test_*.py`).

### Linting & formatting (run all before committing)
```bash
black fitbit_cli/ tests/
isort fitbit_cli/ tests/
pylint fitbit_cli/
mypy fitbit_cli/
```

### CI check (read-only)
```bash
black --check fitbit_cli/ tests/
isort --check-only fitbit_cli/ tests/
```

**Tool settings:** `black` line-length 88; `isort` profile `black`; `pylint` max-line-length 120, `E0401` disabled; `mypy` `ignore_missing_imports = true`. `flake8` and `ruff` are **not used**.

---

## Code Style Guidelines

### General Principles
- Keep code **simple, short, and production-ready**.
- Write as a senior Python developer — readable, direct, no overengineering.
- Do not decompose into too many small functions for the sake of it.
- **Do not change existing code** unless directly required by the task.

### File Header
```python
# -*- coding: utf-8 -*-
"""
Module Description
"""
```

### Imports
- Order: stdlib → third-party (`requests`, `rich`) → relative
- Relative symbol imports: `from .exceptions import FitbitAPIError`
- Module-level alias imports: `from . import formatter as fmt`

### Naming Conventions

| Kind | Convention | Example |
|------|------------|---------|
| Classes | `PascalCase` | `FitbitAPI`, `FitbitInitError` |
| Functions / methods | `snake_case` | `get_sleep_log`, `parse_date_range` |
| Private helpers | `_leading_underscore` | `_create_headers`, `_get_date_range` |
| Constants | `UPPER_SNAKE_CASE` | `BASE_URL`, `TOKEN_URL`, `CONSOLE` |
| Variables | `snake_case` | `start_date`, `access_token` |

### Docstrings
All public classes, methods, and functions must have a one-line docstring. No empty line after `def`.
```python
def get_sleep_log(self, start_date, end_date=None):
    """Get Sleep Logs by Date Range and Date"""
```

### Type Annotations
Not currently used. Do not add unless refactoring a file end-to-end.

### String Formatting
Use f-strings throughout. Never use `%`-formatting or `.format()`.

### Error Handling
- Custom exceptions: `FitbitInitError`, `FitbitAPIError` in `exceptions.py`. Both accept a single `message` arg.
- Use specific exception types; avoid bare `except:`.
- Preserve tracebacks: `raise ... from e`.
- HTTP 401 triggers automatic token refresh inside `make_request()`.

### HTTP Requests
Always include `timeout=5`:
```python
response = requests.request(method, url, headers=self.headers, timeout=5, **kwargs)
```

### Output
- Table mode: always use `CONSOLE.print(...)`. Never call `print()` directly.
- JSON mode: use `print(json.dumps(..., separators=(",", ":")))` for compact output. Never use `rich.print_json()` — it breaks on emoji characters in data.
- Each `display_*` function in `formatter.py` accepts `as_json=False`. When `True`, returns a plain snake_case dict (no printing, no emoji keys). `output.py` collects dicts and prints once.
- Both branches of every `display_*` function must return explicitly (pylint `R1710`).

```python
def display_sleep(sleep_data, as_json=False):
    """Sleep data formatter"""
    if as_json:
        return {"sleep": [...]}
    table = Table(...)
    CONSOLE.print(table)
    return None
```

### pylint Inline Suppression
Use sparingly and only when justified:
```python
# pylint: disable=C0301   # line too long
# pylint: disable=C0413   # import not at top
# pylint: disable=C0103   # invalid variable name
```

---

## CLI Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--init-auth` | `-i` | OAuth2 PKCE setup |
| `--sleep` | `-s` | Sleep log |
| `--spo2` | `-o` | SpO2 summary |
| `--heart` | `-e` | Heart rate time series |
| `--active-zone` | `-a` | Active zone minutes |
| `--breathing-rate` | `-b` | Breathing rate summary |
| `--activities` | `-t` | Daily activity summary |
| `--user-profile` | `-u` | User profile |
| `--devices` | `-d` | Devices list |
| `--json` | `-j` | Output table data as JSON |
| `--raw-json` | `-r` | Full raw JSON response from Fitbit API |
| `--version` | `-v` | Show version |

`--json` and `--raw-json` suppress the spinner and output compact JSON to stdout — designed for AI agent use.

---

## Testing Conventions

- Framework: `unittest.TestCase`, discovered and run by pytest.
- One test class per file, named `Test<Subject>`.
- Each test method has a full docstring.
- Use `unittest.mock.patch` to mock `datetime.today()` for deterministic date tests.
- Add `sys.path.insert(0, ...)` at the top of test files when needed to resolve imports.

---

## CI/CD

- **ci.yml**: Runs on PRs. Executes `super-linter` (black + isort + pylint; flake8/ruff disabled) then `pytest --cov` on Python 3.14.
- **release.yml**: Triggered on GitHub Release creation. Publishes to PyPI via `twine`.
- **dependabot.yml**: Weekly updates for `pip` and `github-actions` dependencies.

---

## Runtime Notes

- OAuth2 PKCE runs a temporary local server on `127.0.0.1:8080` to receive the auth code.
- Token file: `~/.fitbit/token.json` — contains `client_id`, `secret`, `access_token`, `refresh_token`.
- Tokens are valid for 8 hours and auto-refreshed on 401 responses.
- Only GET endpoints are implemented in `FitbitAPI`.
