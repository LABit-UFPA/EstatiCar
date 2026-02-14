from __future__ import annotations

from typing import Callable

import flet as ft


class InputFieldView:
    """Search input field."""

    def __init__(self, on_submit: Callable, page: ft.Page) -> None:
        self._page = page
        self.control = ft.TextField(
            on_submit=lambda e: on_submit(e),
            text_align=ft.TextAlign.LEFT,
            width=self._page.window.width * 0.65,
            height=50,
            label="Digite sua pergunta",
            tooltip="Digite sua pergunta",
        )
