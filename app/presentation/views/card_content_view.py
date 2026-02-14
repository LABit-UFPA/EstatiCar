from __future__ import annotations

import flet as ft


class CardContentView:
    """Displays the main result content (table or placeholder text)."""

    def __init__(self, initial_text: str = "") -> None:
        self.column = ft.Column(controls=[ft.Text(value=initial_text)])

    def build(self) -> ft.Column:
        return self.column
