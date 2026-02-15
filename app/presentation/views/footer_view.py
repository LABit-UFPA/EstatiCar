from __future__ import annotations

import flet as ft

from presentation.components.footer_images import FOOTER_IMAGES


def build_footer() -> ft.Container:
    """Build the modern footer bar with institutional logos."""
    return ft.Container(
        content=ft.Row(
            controls=FOOTER_IMAGES,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=24,
        ),
        padding=ft.padding.symmetric(horizontal=48, vertical=24),
        alignment=ft.alignment.center,
        bgcolor="#ffffff",
        border_radius=16,
        shadow=ft.BoxShadow(
            blur_radius=8,
            spread_radius=0,
            offset=ft.Offset(0, 2),
            color="#0000000a",
        ),
    )
