from __future__ import annotations

from typing import Callable

import flet as ft


def build_train_button(on_click: Callable) -> ft.FilledButton:
    """Build the 'Adicionar Arquivo' button."""
    def handle_click(e):
        on_click()
    
    return ft.FilledButton(
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            side=ft.BorderSide(1, ft.colors.BLUE_ACCENT_100),
            elevation=2,
        ),
        text="Adicionar Arquivo",
        height=50,
        width=260,
        on_click=handle_click,
    )
