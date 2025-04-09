import os
import flet as ft
import pandas as pd
from vanna.remote import VannaDefault

from app.View.tabs_view import TabsView
from app.View.footer_view import FooterView
from app.Themes.themes_data import ThemeData
from app.Components.errors_app import ErrorApp
from app.Components.data_table import data_table
from app.View.card_content_view import CardContentView
from app.View.query_content_view import QueryContentView
from app.Components.progress_dialog import ProgressDialog
from app.View.column_filter_view import ColumnFilterDialog
from app.Controller.load_credentials import load_credentials

def main(page: ft.Page):
    ThemeData(page)
    tabs_container = TabsView(page)
    error_dialog_view = ErrorApp(page)
    filter_dialog_view = ColumnFilterDialog(page)
    last_result = None
    card_view = CardContentView(initial_text="O Resultado será mostrado aqui...")
    card_content = card_view.show_card()
    tabs_container_view = tabs_container.tabs_container_view(card_view)
    progress_dialog = ProgressDialog.progress_dialog

    def set_question(e):
        nonlocal last_result
        prompt = input_field.value
        if prompt.strip():
            progress_dialog.open = True
            page.update()

            jsonFile = load_credentials()
            credentials = jsonFile[0]
            info_database = jsonFile[1]
            path_db_sqlite = info_database['path_db']
            api_key = credentials['api_key_vanna']
            vanna_model_name = credentials['vanna_model_name']
            
            vn = VannaDefault(model=vanna_model_name, api_key=api_key)
            vn.connect_to_sqlite(path_db_sqlite)
            result = vn.ask(prompt, visualize=False, print_results=False, allow_llm_to_see_data=True)
            last_result = result[1]
            table = data_table(result[1])

            if type(result[1]) == pd.DataFrame and not result[1].empty:
                card_content.controls = [
                    ft.Text("Resultado da pesquisa: \n"),
                    table
                ]
                QueryContentView.query_content.controls = [ft.Text("Query uilizada para a pesquisa: \n\n" + result[0]),]

                progress_dialog.open = False
                card_content.update()
                page.update()
            else:
                progress_dialog.open = False
                error_dialog_view.show_error_dialog()

    file_picker = ft.FilePicker(on_result=None)
    page.file_picker = file_picker
    page.add(file_picker)

    def download_table():
        if last_result is not None:
            def on_result(e):
                if e.path:
                    try:
                        save_path = f"{e.path}.xlsx"
                        last_result.to_excel(save_path, index=False)

                        if os.name == 'nt':  # Se for Windows, tenta abrir o diretório
                            os.startfile(os.path.dirname(save_path))

                        msg = "Tabela salva com sucesso."
                    except Exception as ex:
                        msg = f"Erro ao salvar: {ex}"

                    snack_bar = ft.SnackBar(ft.Text(msg))
                    snack_bar.open = True
                    page.update()

            page.file_picker.on_result = on_result
            page.file_picker.save_file()
        else:
            snack_bar = ft.SnackBar(ft.Text("Nenhum resultado encontrado para salvar"))
            snack_bar.open = True
            page.update()

    input_field = ft.TextField(
        text_align=ft.TextAlign.LEFT,
        width=page.window.width * .65,
        height=50,
        label="Digite sua pergunta",
        tooltip="Digite sua pergunta",
        on_submit=set_question
    )

    train_floating_button = ft.FilledButton(
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            side=ft.BorderSide(1, ft.colors.BLUE_ACCENT_100),
            elevation=2
        ),
        text="Adicionar Arquivo",
        height=50,
        width=260,
        on_click=lambda _: filter_dialog_view.open()
    )

    download_table_floating_button = ft.FilledButton(
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            side=ft.BorderSide(1, ft.colors.BLUE_ACCENT_100),
            elevation=2
        ),
        text="Salvar Tabela",
        height=50,
        width=260,
        on_click=lambda _: download_table()
    )

    page.add(
        ft.Stack(
            controls=[
                ft.Container(
                    height=page.window.height,
                    width=page.window.width,
                    padding=ft.padding.all(20),
                    alignment=ft.alignment.center,
                    content=ft.ResponsiveRow([
                        ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        input_field,
                                        ft.IconButton(
                                            icon=ft.icons.SEARCH,
                                            on_click=set_question
                                        )
                                    ]
                                ),
                                ft.SelectionArea(tabs_container_view),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        train_floating_button,
                                        download_table_floating_button
                                    ],
                                ),
                                FooterView.footer
                            ],
                        ),
                    ]),
                ),
            ],
        )
    )

ft.app(target=main)
