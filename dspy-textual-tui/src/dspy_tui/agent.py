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