from __future__ import annotations

import flet as ft


def build_progress_dialog() -> ft.AlertDialog:
    """Create a modern modal progress dialog."""
    return ft.AlertDialog(
        modal=True,
        bgcolor="#ffffff",
        content=ft.Container(
            content=ft.Column(
                [
                    ft.ProgressRing(width=64, height=64, color="#6366f1", stroke_width=4),
                    ft.Text(
                        "Processando...",
                        size=16,
                        weight=ft.FontWeight.W_500,
                        color="#64748b",
                    ),
                ],
                spacing=16,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            width=160,
            height=160,
            padding=ft.padding.all(24),
            border_radius=20,
            shadow=ft.BoxShadow(
                blur_radius=20,
                spread_radius=0,
                offset=ft.Offset(0, 4),
                color="#00000019",
            ),
        ),
    )
