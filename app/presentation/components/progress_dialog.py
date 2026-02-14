from __future__ import annotations

import flet as ft


def build_progress_dialog() -> ft.AlertDialog:
    """Create a modal progress ring dialog."""
    return ft.AlertDialog(
        modal=True,
        content=ft.Container(
            content=ft.ProgressRing(width=60, height=60),
            alignment=ft.alignment.center,
            width=100,
            height=100,
        ),
    )
