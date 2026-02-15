from __future__ import annotations

import flet as ft


class CardContentView:
    """Displays the main result content with modern styling."""

    def __init__(self, initial_text: str = "") -> None:
        self.column = ft.Column(
            controls=[
                ft.Text(
                    value=initial_text,
                    size=14,
                    color="#94a3b8",
                    weight=ft.FontWeight.W_400,
                    italic=True,
                )
            ]
        )

    def build(self) -> ft.Column:
        return self.column
