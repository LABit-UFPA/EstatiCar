import flet as ft

class ThemeData:
    
    def __init__(self, page: ft.Page):
        page.title = "FlechaSQL"
        page.theme_mode = "light"
        page.padding = 0
        page.window.icon = "../assets/images/icon_pcpa_logo.ico"
        page.window.width = 1366
        page.window.height = 900
        page.window.min_width = 600
        page.window.min_height = 700
        page.window.resizable = True
        page.window.maximizable = True
        page.window.maximized = True
        page.window.center()

        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER