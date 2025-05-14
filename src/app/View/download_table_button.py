import flet as ft

class DownloadTableButtonView:
    def __init__(self, event_handler=None):
        self.download_button = ft.FilledButton(
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            side=ft.BorderSide(1, ft.colors.BLUE_ACCENT_100),
            elevation=2
        ),
        text="Salvar Tabela",
        height=50,
        width=260,
        on_click= event_handler
    )

    def download_table_view(self):
        print("download_table")
        return self.download_button