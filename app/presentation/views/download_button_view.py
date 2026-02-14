from __future__ import annotations

from typing import Callable

import flet as ft


def build_download_button(on_click: Callable) -> ft.FilledButton:
    """Build the 'Salvar Tabela' button."""
    return ft.FilledButton(
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            side=ft.BorderSide(1, ft.colors.BLUE_ACCENT_100),
            elevation=2,
        ),
        text="Salvar Tabela",
        height=50,
        width=260,
        on_click=on_click,
    )
