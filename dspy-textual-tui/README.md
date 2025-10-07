# DSPy Textual TUI

Minimal TUI for interacting with a DSPy program. Works on Windows and WSL.

## Prereqs
- Python 3.10+
- [uv](https://github.com/astral-sh/uv)
- Optional: Ollama running locally or API creds for an LLM

## Setup (Windows/WSL paths)
```bash
# choose a workspace under your Windows profile (mounted at /c in your WSL)
mkdir -p /c/Users/user/dev && cd /c/Users/user/dev

# clone or create project folder
mkdir dspy-textual-tui && cd dspy-textual-tui

# write files from this repo structure, then:
uv sync
cp .env.example .env
```

Edit `.env` to choose a backend. Examples:

```env
# Option A: Ollama local chat model
DSPY_BACKEND=ollama
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=llama3.1:8b

# Option B: OpenAI-compatible endpoint
# DSPY_BACKEND=openai
# OPENAI_API_KEY=sk-...
# OPENAI_MODEL=gpt-4o-mini
```

## Run

```bash
uv run python -m dspy_tui.main
```

## Keys

- Type a prompt. Press Enter to run.
- Ctrl+C to quit.

## Tests and quality

```bash
uv run pytest
uv run ruff check src
uv run mypy src
uv run bandit -r src
```
