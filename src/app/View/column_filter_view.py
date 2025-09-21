import flet as ft
from Controller.process_data_table import ProcessDataTable

class ColumnFilterDialog():
    def __init__(self, page: ft.Page):
        self.page = page
        self.process_data_table = ProcessDataTable(self.page)
        self.table = self.process_data_table.get_df()

        self.choice_llms = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="Mistral", label="Mistral"),
                ft.Radio(value="llama", label="llama"),
            ])
        )
        
        self.original_exclude_values = []
        self.original_include_values = []
        
        self.exclude_filter = ft.TextField(label="Pesquisar coluna", on_change=self.filter_exclude)
        self.include_filter = ft.TextField(label="Pesquisar coluna", on_change=self.filter_include)

    def handle_button_click(self):
        self.process_data_table.resetLists()
        self.process_data_table.file_picker.pick_files(allow_multiple=False, allowed_extensions=["xlsx"])

        self._update_original_lists()

    def _extract_text_from_control(self, control):
        """Extrai o texto de diferentes tipos de controles Flet"""
        if control is None:
            return ""
        
        if hasattr(control, 'text') and control.text is not None:
            return control.text
        
        if hasattr(control, 'value') and control.value is not None:
            return control.value
        
        if hasattr(control, 'content'):
            if hasattr(control.content, 'value') and control.content.value is not None:
                return control.content.value
            if hasattr(control.content, 'text') and control.content.text is not None:
                return control.content.text
        
        if isinstance(control, str):
            return control
            
        return ""

    def _update_original_lists(self):
        """Atualiza as listas originais com os valores atuais"""
        self.original_exclude_values = [
            self._extract_text_from_control(item)
            for item in self.process_data_table.exclude_list.controls
            if item is not None
        ]
        self.original_include_values = [
            self._extract_text_from_control(item)
            for item in self.process_data_table.include_list.controls
            if item is not None
        ]

    def _create_filtered_view(self, original_values, query):
        """Cria uma view filtrada dos valores sem modificar a lista original"""
        if not query:
            return [
                ft.TextButton(text=item, on_click=self._handle_item_click) 
                for item in original_values if item
            ]
        
        query_lower = query.lower()

        return [
            ft.TextButton(text=item, on_click=self._handle_item_click) 
            for item in original_values 
            if item and query_lower in item.lower()
        ]

    def _handle_item_click(self, e):
        """Handler personalizado que atualiza as listas originais e depois a visualização"""
        btn = e.control
        item_text = btn.text
        
        if item_text in self.original_exclude_values:
            self.original_exclude_values.remove(item_text)
            if item_text not in self.original_include_values:
                self.original_include_values.append(item_text)
        elif item_text in self.original_include_values:
            self.original_include_values.remove(item_text)
            if item_text not in self.original_exclude_values:
                self.original_exclude_values.append(item_text)
        
        self._refresh_filtered_views()

    def _refresh_filtered_views(self):
        """Atualiza ambas as visualizações baseadas no filtro atual"""
        exclude_query = self.exclude_filter.value if self.exclude_filter.value else ""
        include_query = self.include_filter.value if self.include_filter.value else ""
        
        exclude_filtered = self._create_filtered_view(self.original_exclude_values, exclude_query)
        self.process_data_table.exclude_list.controls = exclude_filtered
        
        include_filtered = self._create_filtered_view(self.original_include_values, include_query)
        self.process_data_table.include_list.controls = include_filtered
        
        self.page.update()

    def _restore_original_buttons(self, values_list, target_list):
        """Restaura os botões originais para permitir interação"""
        if not values_list:
            return
            
        target_list.controls.clear()
        for value in values_list:
            if value:
                btn = ft.TextButton(
                    text=value, 
                    on_click=self.process_data_table.toggle_item
                )
                target_list.controls.append(btn)

    def filter_exclude(self, e):
        """Filtra a visualização da lista de exclusão"""
        if not self.original_exclude_values:
            self._update_original_lists()
        
        query = self.exclude_filter.value if self.exclude_filter.value else ""
        
        filtered_controls = self._create_filtered_view(self.original_exclude_values, query)
        self.process_data_table.exclude_list.controls = filtered_controls
        
        self.page.update()

    def filter_include(self, e):
        """Filtra a visualização da lista de inclusão"""
        if not self.original_include_values:
            self._update_original_lists()
        
        query = self.include_filter.value if self.include_filter.value else ""
        
        filtered_controls = self._create_filtered_view(self.original_include_values, query)
        self.process_data_table.include_list.controls = filtered_controls
        
        self.page.update()

    def restore_original_view(self):
        """Restaura a visualização original das listas (sem filtro)"""
        if self.original_exclude_values:
            self.process_data_table.exclude_list.controls = self._create_filtered_view(
                self.original_exclude_values, ""
            )
        if self.original_include_values:
            self.process_data_table.include_list.controls = self._create_filtered_view(
                self.original_include_values, ""
            )
        
        self.exclude_filter.value = ""
        self.include_filter.value = ""
        
        self.page.update()

    def build(self):
        self._update_original_lists()
        
        exclude_container = ft.Container(
            content=ft.Column([
                ft.Text("Colunas Removidas:", size=16, weight=ft.FontWeight.BOLD, color="red600"),
                self.exclude_filter,
                ft.Container(self.process_data_table.exclude_list, border=ft.border.all(1), padding=10, height=150),
            ]),
            border=ft.border.all(2, ft.colors.RED),
            padding=10,
            expand=1
        )

        include_container = ft.Container(
            content=ft.Column([
                ft.Text("Colunas Selecionadas:", size=16, weight=ft.FontWeight.BOLD, color="green600"),
                self.include_filter,
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
                    on_click=lambda _: self._handle_training(),
                )
            ]
        )

    def _handle_training(self):
        """Inicia o treinamento sincronizando primeiro com ProcessDataTable"""

        self.process_data_table.exclude_list.controls = [
            ft.TextButton(text=item, on_click=self.process_data_table.toggle_item)
            for item in self.original_exclude_values
        ]
        self.process_data_table.include_list.controls = [
            ft.TextButton(text=item, on_click=self.process_data_table.toggle_item)
            for item in self.original_include_values
        ]
        
        self.process_data_table.init_process_files(self.choice_llms.value)

    def open(self):
        self.dialog = self.build()
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()