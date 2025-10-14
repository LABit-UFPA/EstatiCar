import flet as ft
from Controller.process_data_table import ProcessDataTable
from Controller.process_data_table import ProcessDataTable
from Components.DropDownComponentMenu import DropdownMenuComponent
class ColumnFilterDialog():
    def __init__(self, page: ft.Page, state):
        self.page = page
        self.process_data_table = ProcessDataTable(self.page)
        self.table = self.process_data_table.get_df()
        self.choice_llms = DropdownMenuComponent(
                    page=self.page,
                    options=["mistral:latest", "llama3.1:latest", "gemma3:4b", "smollm2:1.7b", "qwen3:4b"],
                    label="Escolha o modelo de IA",
                    event_handler=lambda e: self._update_choice(e, state)
                ).dropdown_menu_view()
        
    def _update_choice(self, e, state):
        state.choice = e.control.value
        print(f"Modelo selecionado: {e.control.value}")
        
    def handle_button_click(self):
        self.process_data_table.resetLists()
        self.process_data_table.file_picker.pick_files(allow_multiple=False, allowed_extensions=["xlsx"])

    def build(self):        
        exclude_container = ft.Container(
            content=ft.Column([
                ft.Text("Colunas Removidas:", size=16, weight=ft.FontWeight.BOLD, color="red600"),
                ft.Container(self.process_data_table.exclude_list, border=ft.border.all(1), padding=10, height=150),
            ]),
            border=ft.border.all(2, ft.colors.RED),
            padding=10,
            expand=1
        )

        include_container = ft.Container(
            content=ft.Column([
                ft.Text("Colunas Selecionadas:", size=16, weight=ft.FontWeight.BOLD, color="green600"),
                ft.Container(self.process_data_table.include_list, border=ft.border.all(1), padding=10, height=150),
            ]),
            border=ft.border.all(2, ft.colors.GREEN),
            padding=10,
            expand=1
        )

        buttons = ft.Column([
            ft.ElevatedButton("→", on_click=self.process_data_table.move_to_include),
            ft.ElevatedButton(">>", on_click=self.process_data_table.move_all_to_include),
            ft.ElevatedButton("<<", on_click=self.process_data_table.move_all_to_exclude),
            ft.ElevatedButton("←", on_click=self.process_data_table.move_to_exclude),
        ])

        return ft.AlertDialog(
            title=ft.Text("Filtrar Colunas", weight=ft.FontWeight.BOLD,),
            content=ft.Container(
                height=600,
                width=600,
                content=ft.Column([
                    ft.FilledButton(
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            side=ft.BorderSide(1, ft.colors.BLUE_ACCENT_100),
                            elevation=2
                        ),
                        text="Selecionar arquivo", height=50, width=260,
                        on_click=lambda _: self.handle_button_click()
                    ),
                    ft.Row([exclude_container, buttons, include_container]),
                    ft.Text(
                        "Escolha qual IA quer utilizar:", 
                        size=16, 
                        weight=ft.FontWeight.BOLD,
                    ),
                    self.choice_llms,])
            ),
            actions=[
                ft.FilledButton(
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        side=ft.BorderSide(1, ft.colors.BLUE_ACCENT_100),
                        elevation=2
                    ),
                    text= "Realizar Treinamento", height=50, width=260,
                    on_click=lambda _: self.process_data_table.init_process_files(self.choice_llms.value),
                )
            ]
        )

    def open(self):
        self.dialog = self.build()
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()