import flet as ft

class TrainButtonView:
    def __init__(self, page: ft.Page, event_handler):
        self.page = page
        self.train_button = ft.FilledButton(
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            side=ft.BorderSide(1, ft.colors.BLUE_ACCENT_100),
            elevation=2
        ),
        text="Adicionar Arquivo",
        height=50,
        width=260,
        on_click= lambda _: event_handler()
    )

    def train_button_view(self):
        print("train_button_view")
        return self.train_button
