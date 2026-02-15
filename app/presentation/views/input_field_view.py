from __future__ import annotations

from typing import Callable

import flet as ft


class InputFieldView:
    """Modern search input field."""

    def __init__(self, on_submit: Callable, page: ft.Page) -> None:
        self._page = page
        self.text_field = ft.TextField(
            on_submit=lambda e: on_submit(e),
            text_align=ft.TextAlign.LEFT,
            width=self._page.window.width * 0.65,
            min_lines=1,
            max_lines=3,
            multiline=True,
            label="Digite sua pergunta",
            hint_text="Pergunte algo sobre seus dados...",
            tooltip="Digite sua pergunta",
            border_radius=16,
            filled=True,
            bgcolor="#ffffff",
            border_color="#e2e8f0",
            focused_border_color="#6366f1",
            focused_bgcolor="#ffffff",
            text_size=16,
            label_style=ft.TextStyle(size=14, color="#64748b"),
            content_padding=ft.padding.symmetric(horizontal=20, vertical=16),
        )
        
        # Use the text field directly (shadow removed to prevent height issues)
        self.control = self.text_field

