from __future__ import annotations
import dspy


class Answer(dspy.Signature):
    """Answer a user prompt briefly."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="concise response")