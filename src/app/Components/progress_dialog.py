import flet as ft

class ProgressDialog:

    progress_dialog = ft.AlertDialog(
        modal=True,
        content=ft.Container(
            content=ft.ProgressRing(width=60, height=60),
            alignment=ft.alignment.center,
            width=100,
            height=100,
        ),
    )