import flet as ft

class CardContentView:
    def __init__(self, initial_text = ""):
        self.initial_text = initial_text
        self.column = ft.Column(controls=[ft.Text(value=self.initial_text)])
    


    def show_card(self):
        return self.column