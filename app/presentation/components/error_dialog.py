from __future__ import annotations

import flet as ft


class ErrorDialog:
    """Standardized error dialog component."""

    def __init__(self, page: ft.Page) -> None:
        self._page = page
        self._dialog = self._build()

    def _build(self) -> ft.AlertDialog:
        return ft.AlertDialog(
            actions=[
                ft.TextButton(
                    "Entendido",
                    on_click=lambda e: self.close(),
                    style=ft.ButtonStyle(
                        color=ft.colors.WHITE,
                        bgcolor=ft.colors.RED,
                        padding=ft.padding.symmetric(horizontal=16, vertical=8),
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                )
            ],
            modal=True,
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.ERROR_OUTLINE, size=48, color=ft.colors.RED),
                        ft.Text(
                            "Erro ao realizar a pesquisa!",
                            style=ft.TextStyle(
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.BLACK,
                            ),
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            "Por favor, reformule a sua pesquisa.",
                            style=ft.TextStyle(size=14, color=ft.colors.BLACK87),
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    spacing=12,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                width=350,
                height=200,
                padding=ft.padding.all(16),
                bgcolor=ft.colors.WHITE,
                border_radius=12,
                shadow=ft.BoxShadow(
                    blur_radius=10,
                    spread_radius=1,
                    offset=ft.Offset(0, 2),
                    color=ft.colors.BLACK12,
                ),
            ),
        )

    def show(self) -> None:
        # Use inline notification for web compatibility
        if hasattr(self._page, 'show_notification'):
            self._page.show_notification("Erro ao realizar a pesquisa!", ft.colors.RED, duration=5)

    def close(self) -> None:
        if self._page.snack_bar:
            self._page.snack_bar.open = False
            self._page.update()

