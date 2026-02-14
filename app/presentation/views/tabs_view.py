from __future__ import annotations

import flet as ft

from presentation.views.query_content_view import QueryContentView


class TabsView:
    """Tab container with Table and Query tabs."""

    def __init__(self, page: ft.Page) -> None:
        self._page = page

    def build(
        self,
        card_content: ft.Column,
        query_content: ft.Column,
    ) -> ft.Container:
        return ft.Container(
            alignment=ft.alignment.center,
            padding=10,
            width=self._page.window.width * 0.7,
            height=self._page.window.height * 0.33,
            content=ft.Tabs(
                selected_index=0,
                animation_duration=300,
                expand=True,
                tab_alignment=ft.TabAlignment.CENTER,
                tabs=[
                    ft.Tab(
                        text="Tabela",
                        icon=ft.Icons.TABLE_VIEW,
                        content=ft.Container(
                            content=ft.Column(
                                scroll="ADAPTIVE",
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[card_content],
                            ),
                        ),
                    ),
                    ft.Tab(
                        text="Query",
                        icon=ft.Icons.MANAGE_SEARCH_OUTLINED,
                        content=ft.Container(
                            content=ft.Column(
                                scroll="ADAPTIVE",
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[query_content],
                            ),
                        ),
                    ),
                ],
            ),
        )
