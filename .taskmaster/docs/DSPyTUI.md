```
\\ path: dspy-textual-tui_starter_windows_wsl.md
# DSPy Textual TUI — Windows/WSL Starter

A minimal Textual-based TUI that wraps a tiny DSPy module. Uses `uv` for env, your WSL path convention, and your Python tooling.

## Tree
```

dspy-textual-tui/
├─ pyproject.toml
├─ README.md
├─ .env.example
├─ src/
│  └─ dspy_tui/
│     ├─ __init__.py
│     ├─ lm_config.py
│     ├─ signatures.py
│     ├─ agent.py
│     └─ main.py
└─ tests/
   └─ test_agent.py

```

## Files

```toml
# path: pyproject.toml
[project]
name = "dspy-textual-tui"
version = "0.1.0"
description = "Textual TUI wrapper for a minimal DSPy agent"
readme = "README.md"
requires-python = ">=3.10"
authors = [{name = "You"}]
license = {text = "MIT"}

[project.dependencies]
dspy-ai = "*"
textual = "*"
loguru = "*"
python-dotenv = "*"

[tool.uv]
# uv will read this to resolve and create the environment

[tool.ruff]
line-length = 100

[tool.mypy]
python_version = "3.10"
warn_unused_configs = true
strict = true

[tool.pytest.ini_options]
addopts = "-q"

[tool.bandit]
targets = ["src"]
```

```markdown
# path: README.md
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

```
```toml
# path: .env.example
# Backend selection: "ollama" or "openai"
DSPY_BACKEND=ollama

# Ollama settings
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=llama3.1:8b

# OpenAI-compatible settings (if used)
# OPENAI_API_KEY=
# OPENAI_MODEL=gpt-4o-mini
```

```python
# path: src/dspy_tui/__init__.py
"""Package init for DSPy Textual TUI."""
```

```python
# path: src/dspy_tui/lm_config.py
from __future__ import annotations
import os
from loguru import logger
import dspy


def configure_lm() -> None:
    """Configure DSPy LM from environment variables.

    Supports two backends:
      - DSPY_BACKEND=ollama  → uses local Ollama chat endpoint
      - DSPY_BACKEND=openai  → uses OpenAI-compatible API
    """
    backend = os.getenv("DSPY_BACKEND", "ollama").lower()

    if backend == "ollama":
        base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        model = os.getenv("MODEL_NAME", "llama3.1:8b")
        lm = dspy.LM(
            f"ollama_chat/{model}",
            api_base=base,
            api_key="",
            cache=False,
            streaming=False,
        )
        dspy.configure(lm=lm)
        logger.info("Configured DSPy LM via Ollama: {} @ {}", model, base)
        return

    if backend == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required for openai backend")
        lm = dspy.LM(
            model,
            api_key=api_key,
            cache=False,
            streaming=False,
        )
        dspy.configure(lm=lm)
        logger.info("Configured DSPy LM via OpenAI-compatible API: {}", model)
        return

    raise RuntimeError(f"Unsupported DSPY_BACKEND: {backend}")
```

```python
# path: src/dspy_tui/signatures.py
from __future__ import annotations
import dspy


class Answer(dspy.Signature):
    """Answer a user prompt briefly."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="concise response")
```

```python
# path: src/dspy_tui/agent.py
from __future__ import annotations
from loguru import logger
import dspy
from .signatures import Answer


class MiniAgent(dspy.Module):
    """A trivial DSPy module. Replace with your program logic as needed."""

    def __init__(self) -> None:
        super().__init__()
        self.predict = dspy.Predict(Answer)

    def forward(self, prompt: str) -> str:
        logger.debug("MiniAgent.forward prompt={}", prompt)
        out = self.predict(question=prompt)
        return out.answer
```

```python
# path: src/dspy_tui/main.py
from __future__ import annotations
import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Input, Header, Footer, Static
from textual.containers import Vertical
from textual.reactive import reactive
from loguru import logger
from dotenv import load_dotenv

from .lm_config import configure_lm
from .agent import MiniAgent


class Output(Static):
    pass


class DSPyTUI(App):
    CSS_PATH = None
    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
    ]

    thinking: reactive[bool] = reactive(False)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Vertical():
            self.input = Input(placeholder="Ask something and press Enter…")
            self.output = Output("Ready.")
            yield self.input
            yield self.output
        yield Footer()

    async def on_mount(self) -> None:
        load_dotenv()
        configure_lm()
        self.agent = MiniAgent()
        await self.input.focus()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        prompt = event.value.strip()
        if not prompt:
            return
        self.thinking = True
        self.output.update("Thinking…")
        # Run DSPy call in a worker to avoid blocking the UI loop.
        result = await asyncio.to_thread(self.agent.forward, prompt)
        self.output.update(result)
        self.input.value = ""
        self.thinking = False


def main() -> None:
    DSPyTUI().run()


if __name__ == "__main__":
    main()
```

```python
# path: tests/test_agent.py
from __future__ import annotations
from dspy_tui.agent import MiniAgent


def test_forward_returns_str(monkeypatch):
    agent = MiniAgent()

    class Dummy:
        answer = "ok"

    def fake_predict(question: str):  # type: ignore[no-redef]
        return Dummy()

    agent.predict = fake_predict  # type: ignore[assignment]
    assert agent.forward("hi") == "ok"
```

EOF

```
