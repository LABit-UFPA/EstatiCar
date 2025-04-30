import flet as ft

class InputFieldView:
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.input_field = ft.TextField(
            text_align=ft.TextAlign.LEFT,
            width=self.page.window.width * 0.65,
            height=50,
            label="Digite sua pergunta",
            tooltip="Digite sua pergunta"
        )

    def input_field_view(self):
        print("input_field_view")
        return self.input_field
