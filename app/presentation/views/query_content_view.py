from __future__ import annotations

import flet as ft


class QueryContentView:
    """Displays the SQL query used for the last search."""

    def __init__(self) -> None:
        self.column = ft.Column(
            controls=[ft.Text(value="A query para a consulta será mostrada aqui...")],
        )

    def build(self) -> ft.Column:
        return self.column
