from __future__ import annotations

import flet as ft

from presentation.views.query_content_view import QueryContentView


class TabsView:
    """Modern tab container with Table and Query tabs."""

    def __init__(self, page: ft.Page) -> None:
        self._page = page

    def build(
        self,
        card_content: ft.Column,
        query_content: ft.Column,
    ) -> ft.Container:
        return ft.Container(
            alignment=ft.alignment.center,
            padding=20,
            width=self._page.window.width * 0.7,
            height=self._page.window.height * 0.33,
            bgcolor="#ffffff",
            border_radius=20,
            shadow=ft.BoxShadow(
                blur_radius=20,
                spread_radius=0,
                offset=ft.Offset(0, 4),
                color="#0000000d",
            ),
            content=ft.Tabs(
                selected_index=0,
                animation_duration=300,
                expand=True,
                tab_alignment=ft.TabAlignment.CENTER,
                indicator_color="#6366f1",
                indicator_border_radius=8,
                indicator_tab_size=True,
                label_color="#6366f1",
                unselected_label_color="#94a3b8",
                divider_color="#e2e8f0",
                tabs=[
                    ft.Tab(
                        text="Tabela",
                        icon=ft.Icons.TABLE_VIEW_ROUNDED,
                        content=ft.Container(
                            content=ft.Column(
                                scroll="ADAPTIVE",
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[card_content],
                            ),
                            padding=ft.padding.all(16),
                        ),
                    ),
                    ft.Tab(
                        text="Query",
                        icon=ft.Icons.MANAGE_SEARCH_ROUNDED,
                        content=ft.Container(
                            content=ft.Column(
                                scroll="ADAPTIVE",
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[query_content],
                            ),
                            padding=ft.padding.all(16),
                        ),
                    ),
                ],
            ),
        )
