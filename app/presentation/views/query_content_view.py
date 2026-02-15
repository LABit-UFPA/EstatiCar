from __future__ import annotations

import flet as ft


class QueryContentView:
    """Displays the SQL query used for the last search with modern styling."""

    def __init__(self) -> None:
        self.column = ft.Column(
            controls=[
                ft.Text(
                    value="A query para a consulta será mostrada aqui...",
                    size=14,
                    color="#94a3b8",
                    weight=ft.FontWeight.W_400,
                    italic=True,
                )
            ],
        )

    def build(self) -> ft.Column:
        return self.column
