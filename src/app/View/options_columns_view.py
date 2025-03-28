import flet as ft

class OptionsColumnsView:

    def show_page():
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(controls=[
                        ft.Container(
                            bgcolor=ft.colors.YELLOW, 
                            width=300,
                            height=500,
                            content=ft.Column(controls=[ft.Text('Incluir')])
                            ),
                            ft.Container(
                            bgcolor=ft.colors.BLUE, 
                            width=300,
                            height=500,
                            content=ft.Column(
                                controls=[
                                    ft.Card(content=ft.Text('Excluir')),
                                    ft.ListView(controls=[ft.TextButton(text="AAAAAAAAA")])
                                    ]
                                )
                            ),
                            ]
                        ),
                    ]
                )
            )
    