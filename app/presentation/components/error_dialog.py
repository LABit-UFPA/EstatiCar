from __future__ import annotations

import flet as ft


class ErrorDialog:
    """Modern standardized error dialog component."""

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
                        color="#ffffff",
                        bgcolor="#ef4444",
                        padding=ft.padding.symmetric(horizontal=24, vertical=12),
                        shape=ft.RoundedRectangleBorder(radius=10),
                        overlay_color={
                            ft.ControlState.HOVERED: "#dc2626",
                        },
                    ),
                )
            ],
            modal=True,
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.ERROR_OUTLINE_ROUNDED, size=56, color="#ef4444"),
                        ft.Text(
                            "Erro ao realizar a pesquisa!",
                            style=ft.TextStyle(
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color="#1e293b",
                            ),
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            "Por favor, reformule a sua pesquisa.",
                            style=ft.TextStyle(size=15, color="#64748b"),
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    spacing=16,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                width=380,
                height=220,
                padding=ft.padding.all(24),
                bgcolor="#ffffff",
                border_radius=20,
                shadow=ft.BoxShadow(
                    blur_radius=30,
                    spread_radius=0,
                    offset=ft.Offset(0, 8),
                    color="#00000026",
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

