# DSPyTUI

A Textual User Interface for interacting with DSPy programs.

## Overview

DSPyTUI provides a minimal, terminal-based interface for working with DSPy agents. It allows you to chat with a DSPy agent, configure different language model backends, and view the results in a simple, user-friendly TUI.

This project is structured as a Python package within the `dspy-textual-tui` directory, using `uv` for package management and `ruff`, `mypy`, and `bandit` for code quality.

## Features

-   **Textual User Interface:** A simple and intuitive TUI for interacting with a DSPy agent.
-   **Configurable Backends:** Easily switch between different language model backends like Ollama and OpenAI.
-   **Cross-Platform:** Works on Windows, WSL, and other Linux environments.
-   **Code Quality:** Includes a full suite of tools for linting, formatting, type checking, and security scanning.

## Project Structure

```
/
├── .gitignore
├── AGENTS.md
├── GEMINI.md
├── README.md
└── dspy-textual-tui/
    ├── .env.example
    ├── pyproject.toml
    ├── README.md
    ├── src/
    │   └── dspy_tui/
    │       ├── __init__.py
    │       ├── agent.py
    │       ├── lm_config.py
    │       ├── main.py
    │       └── signatures.py
    └── tests/
        └── test_agent.py
```

## Setup

1.  **Prerequisites:**
    *   Python 3.10+
    *   [uv](https://github.com/astral-sh/uv)
    *   An LLM backend (e.g., Ollama running locally or API credentials for a service like OpenAI).

2.  **Installation:**
    ```bash
    # Clone the repository
    git clone <repository-url>
    cd DSPyTUI

    # Create a virtual environment and install dependencies
    uv sync
    ```

3.  **Configuration:**
    *   Copy the example environment file:
        ```bash
        cp dspy-textual-tui/.env.example dspy-textual-tui/.env
        ```
    *   Edit `dspy-textual-tui/.env` to configure your desired backend.

    **Example for Ollama:**
    ```env
    DSPY_BACKEND=ollama
    OLLAMA_BASE_URL=http://localhost:11434
    MODEL_NAME=llama3.1:8b
    ```

    **Example for OpenAI:**
    ```env
    # DSPY_BACKEND=openai
    # OPENAI_API_KEY=sk-...
    # OPENAI_MODEL=gpt-4o-mini
    ```

## Usage

To run the TUI application:

```bash
uv run python -m dspy_tui.main
```

**Controls:**

*   Type your prompt in the input box.
*   Press `Enter` to send the prompt to the agent.
*   Press `Ctrl+C` to exit the application.

## Development

This project uses a suite of tools to ensure code quality.

*   **Testing:**
    ```bash
    uv run pytest
    ```

*   **Linting and Formatting:**
    ```bash
    uv run ruff check src
    uv run ruff format src
    ```

*   **Type Checking:**
    ```bash
    uv run mypy src
    ```

*   **Security Scanning:**
    ```bash
    uv run bandit -r src
    ```
