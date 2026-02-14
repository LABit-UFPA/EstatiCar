from __future__ import annotations

from typing import Any


class AppState:
    """Centralized mutable application state for the presentation layer."""

    def __init__(self) -> None:
        self.last_result: Any = None  # Last DataFrame result
        self.choice: str = "gemma3:4b"  # Currently selected LLM model
