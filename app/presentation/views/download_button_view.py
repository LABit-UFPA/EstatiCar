from __future__ import annotations

from typing import Callable

import flet as ft


def build_download_button(on_click: Callable) -> ft.Container:
    """Build the modern 'Salvar Tabela' button."""
    button = ft.FilledButton(
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            bgcolor="#10b981",
            color="#ffffff",
            elevation=0,
            padding=ft.padding.symmetric(horizontal=24, vertical=16),
            overlay_color={
                ft.ControlState.HOVERED: "#059669",
                ft.ControlState.PRESSED: "#047857",
            },
        ),
        text="Salvar Tabela",
        icon=ft.Icons.DOWNLOAD_ROUNDED,
        height=54,
        width=270,
        on_click=on_click,
    )
    
    return ft.Container(
        content=button,
        shadow=ft.BoxShadow(
            blur_radius=12,
            spread_radius=0,
            offset=ft.Offset(0, 4),
            color="#10b98133",
        ),
    )
