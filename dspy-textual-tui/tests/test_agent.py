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