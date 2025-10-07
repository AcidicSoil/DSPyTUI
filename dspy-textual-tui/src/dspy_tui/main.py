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