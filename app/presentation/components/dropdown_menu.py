from __future__ import annotations

from typing import Callable

import flet as ft


class DropdownMenu:
    """Modern reusable dropdown menu component."""

    def __init__(
        self,
        page: ft.Page,
        options: list[str],
        label: str,
        on_change: Callable,
    ) -> None:
        self._page = page
        self.control = ft.Dropdown(
            options=[ft.dropdown.Option(opt) for opt in options],
            value=options[0] if options else None,
            width=300,
            on_change=on_change,
            label=label,
            border_radius=12,
            filled=True,
            bgcolor="#f8fafc",
            border_color="#e2e8f0",
            focused_border_color="#6366f1",
            text_size=14,
            label_style=ft.TextStyle(size=13, color="#64748b"),
        )
