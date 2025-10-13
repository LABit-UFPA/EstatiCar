import flet as ft

class DropdownMenuComponent:
    
    def __init__(self, page: ft.Page, options: list[str], label: str, event_handler: callable):
        self.page = page
        self.options = options
        self.label = label
        self.dropdown_menu = ft.Dropdown(
            options=[ft.dropdown.Option(option) for option in self.options],
            value=self.options[0] if self.options else None,
            width=200,
            on_change=event_handler,
            label=self.label
        )

    def dropdown_menu_view(self):
        return self.dropdown_menu