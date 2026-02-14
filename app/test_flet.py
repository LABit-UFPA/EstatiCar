import flet as ft

def main(page: ft.Page):
    page.title = "Teste Flet"
    page.window.width = 800
    page.window.height = 600
    
    page.add(
        ft.Column([
            ft.Text("Hello World!", size=30, color="blue"),
            ft.ElevatedButton("Click me", on_click=lambda e: print("Clicked!")),
        ])
    )
    page.update()

ft.app(target=main)
