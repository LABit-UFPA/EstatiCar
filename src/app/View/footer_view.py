import flet as ft
from Components.footer_components import Footer


class FooterView:
    
    footer = ft.Container(
        content=ft.Row(
            controls= Footer.footer_images,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=40,
        alignment=ft.alignment.center,
        bgcolor='transparent',
    )