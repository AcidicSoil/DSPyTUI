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