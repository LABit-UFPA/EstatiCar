from __future__ import annotations

from typing import Callable

import flet as ft


def build_train_button(on_click: Callable) -> ft.Container:
    """Build the modern 'Adicionar Arquivo' button."""
    def handle_click(e):
        on_click()
    
    button = ft.FilledButton(
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            bgcolor="#6366f1",
            color="#ffffff",
            elevation=0,
            padding=ft.padding.symmetric(horizontal=24, vertical=16),
            overlay_color={
                ft.ControlState.HOVERED: "#5558e3",
                ft.ControlState.PRESSED: "#4a4dd6",
            },
        ),
        text="Adicionar Arquivo",
        icon=ft.Icons.UPLOAD_FILE_ROUNDED,
        height=54,
        width=270,
        on_click=handle_click,
    )
    
    return ft.Container(
        content=button,
        shadow=ft.BoxShadow(
            blur_radius=12,
            spread_radius=0,
            offset=ft.Offset(0, 4),
            color="#6366f133",
        ),
    )
