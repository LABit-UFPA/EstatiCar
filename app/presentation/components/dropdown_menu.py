from __future__ import annotations

from typing import Callable

import flet as ft


class DropdownMenu:
    """Reusable dropdown menu component."""

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
            width=200,
            on_change=on_change,
            label=label,
        )
