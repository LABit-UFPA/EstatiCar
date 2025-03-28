import flet as ft

class ErrorApp:
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.error_dialog = self.errorDialog()

    def close_error_dialog(self):
        self.error_dialog.open = False
        self.page.update()

    def show_error_dialog(self):
        self.page.dialog = self.error_dialog
        self.error_dialog.open = True
        self.page.update()

    def errorDialog(self):
            return ft.AlertDialog(
            actions=[
                ft.TextButton(
                    "Entendido",
                    on_click=lambda e: self.close_error_dialog(),
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
                        ft.Icon(ft.icons.ERROR_OUTLINE, size=48, color=ft.colors.RED),
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