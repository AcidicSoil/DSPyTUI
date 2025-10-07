# Task Master AI - Agent Integration Guide

## Python Tooling

- Package Management & Virtual Envs: `uv`
  (fast replacement for pip/pip-tools/virtualenv; use `uv pip install ...`, `uv run ...`)
- Linting & Formatting: `ruff`
  (linter + formatter; use `ruff check .`, `ruff format .`)
- Static Typing: `mypy`
  (type checking; use `mypy .`)
- Security: `bandit`
  (Python security linter; use `bandit -r .`)
- Testing: `pytest`
  (test runner; use `pytest -q`, `pytest -k <pattern>` to filter tests)
- Logging: `loguru`
  (runtime logging utility; import in code:

  ```python
  from loguru import logger
  logger.info("message")
  ```)

## Notes

- Prefer uv for Python dependency and environment management instead of pip/venv/poetry/pip-tools.
