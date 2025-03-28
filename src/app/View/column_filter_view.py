import flet as ft
from app.Controller.process_data_table import ProcessDataTable

class ColumnFilterDialog():
    def __init__(self, page: ft.Page):
        self.page = page
        self.process_data_table = ProcessDataTable(self.page)
        self.table = self.process_data_table.get_df()

        self.api_key_vanna = ft.TextField(label="API Key Vanna", visible=False)
        self.model_name_vanna = ft.TextField(label="Model Name Vanna", visible=False)

        self.api_key_gemini = ft.TextField(label="API Key Gemini", visible=False)
        self.model_name_gemini = ft.TextField(label="Model Name Gemini", visible=False)

        self.choice_llms = ft.RadioGroup(
            on_change=self.toggle_fields,
            content=ft.Row([
                ft.Radio(value="Vanna", label="Vanna"),
                # ft.Radio(value="Gemini", label="Gemini")
            ])
        )

        self.exclude_filter = ft.TextField(label="Filter", on_change=self.filter_exclude)
        self.include_filter = ft.TextField(label="Filter", on_change=self.filter_include)

    def toggle_fields(self, e):
        selected = self.choice_llms.value
        is_vanna = selected == "Vanna"
        is_gemini = selected == "Gemini"

        self.api_key_vanna.visible = is_vanna or is_gemini
        self.model_name_vanna.visible = is_vanna or is_gemini

        self.api_key_gemini.visible = is_gemini
        self.model_name_gemini.visible = is_gemini

        self.page.update()

    def filter_exclude(self, e):
        """Filtra os itens da lista de exclusão sem perder os dados originais."""
        if not self.process_data_table.exclude_list or not self.process_data_table.exclude_list.controls:
            return

        original_exclude_values = [
            item.content.value for item in self.process_data_table.exclude_list.controls if item and item.content
        ]

        query = self.exclude_filter.value.lower()
        self.process_data_table.exclude_list.controls = [
            ft.Text(value=item) for item in original_exclude_values if query in item.lower()
        ]
        
        print("exclude_list:", self.process_data_table.exclude_list)
        print("exclude_list.controls:", getattr(self.process_data_table.exclude_list, "controls", None))


        self.page.update()


    def filter_include(self, e):
        """Filtra os itens da lista de inclusão sem perder os dados originais."""
        if not self.process_data_table.include_list or not self.process_data_table.include_list.controls:
            return

        original_include_values = [
            item.content.value for item in self.process_data_table.include_list.controls if item and item.content
        ]

        query = self.include_filter.value.lower()
        self.process_data_table.include_list.controls = [
            ft.Text(value=item) for item in original_include_values if query in item.lower()
        ]
        print("include_list:", self.process_data_table.include_list)
        print("include_list.controls:", getattr(self.process_data_table.include_list, "controls", None))

        self.page.update()


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
            ft.ElevatedButton("←", on_click=self.process_data_table.move_to_exclude)
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
                        on_click=lambda _: self.process_data_table.file_picker.pick_files(allow_multiple=False, allowed_extensions=["xlsx"])
                    ),
                    ft.Row([exclude_container, buttons, include_container]),
                    ft.Text(
                        "Escolha qual IA quer utilizar:", 
                        size=16, 
                        weight=ft.FontWeight.BOLD,
                    ),
                    self.choice_llms,
                    ft.Container(
                        width=200,
                        content=ft.Column(
                            alignment=ft.alignment.center,
                            controls=[
                                self.api_key_vanna,
                                self.model_name_vanna,
                                self.api_key_gemini,
                                self.model_name_gemini])
                                )]
                            )
            ),
            actions=[
                ft.FilledButton(
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        side=ft.BorderSide(1, ft.colors.BLUE_ACCENT_100),
                        elevation=2
                    ),
                    text= "Realizar Treinamento", height=50, width=260,
                    on_click=lambda _: self.process_data_table.init_process_files(
                        self.choice_llms.value, self.api_key_vanna.value, self.model_name_vanna.value,
                        self.api_key_gemini.value, self.model_name_gemini.value
                    ),

                )
            ]
        )

    def open(self):
        self.dialog = self.build()
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()
