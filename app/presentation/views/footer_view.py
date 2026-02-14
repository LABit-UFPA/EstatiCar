from __future__ import annotations

import flet as ft

from presentation.components.footer_images import FOOTER_IMAGES


def build_footer() -> ft.Container:
    """Build the footer bar with institutional logos."""
    return ft.Container(
        content=ft.Row(
            controls=FOOTER_IMAGES,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=40,
        alignment=ft.alignment.center,
        bgcolor="transparent",
    )
