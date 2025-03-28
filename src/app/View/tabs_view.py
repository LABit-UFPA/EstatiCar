import flet as ft
from app.View.query_content_view import QueryContentView

class TabsView:

    def __init__(self, page: ft.Page):
        self.page = page

    def tabs_container_view(self, card_view):
        return ft.Container(
        alignment=ft.alignment.center,
        padding=10,
        width=self.page.window.width*.7,
        height=self.page.window.width*.33,
        content=ft.Tabs(
            selected_index=0,
            animation_duration=300,
            expand=True,
            tab_alignment=ft.TabAlignment.CENTER,
            tabs=[
                ft.Tab(
                    text="Tabela",
                    icon=ft.icons.TABLE_VIEW,
                    content=ft.Container(
                        content=ft.Column(
                            scroll="ADAPTIVE",
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[card_view.show_card()],
                        ),
                    ),
                ),
                ft.Tab(
                    text="Query",
                    icon=ft.icons.MANAGE_SEARCH_OUTLINED,
                    content=ft.Container(
                        content=ft.Column(
                            scroll="ADAPTIVE",
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[QueryContentView.query_content],
                        ),
                    ),
                ),
            ],
        ),
    )