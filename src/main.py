import os
import flet as ft
import pandas as pd
from vanna.remote import VannaDefault

from app.View.tabs_view import TabsView
from app.View.footer_view import FooterView
from app.Themes.themes_data import ThemeData
from app.Components.errors_app import ErrorApp
from app.Components.data_table import data_table
from app.View.input_field_view import InputFieldView
from app.View.card_content_view import CardContentView
from app.View.query_content_view import QueryContentView
from app.Components.progress_dialog import ProgressDialog
from app.View.column_filter_view import ColumnFilterDialog
from app.Controller.load_credentials import load_credentials


from app.View.train_button import TrainButtonView
from app.Controller.download_table import download_table
from app.View.download_table_button import DownloadTableButtonView

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
    input_field = InputFieldView(page)
    input_field_view = input_field.input_field_view()

    train_floating_button_view = TrainButtonView(page, filter_dialog_view.open).train_button_view()

    download_table_floating_button = DownloadTableButtonView(event_handler=lambda e: download_table(page, last_result))
    download_table_floating_button_view = download_table_floating_button.download_table_view()

    def set_question(e):
        nonlocal last_result
        prompt = input_field_view.value
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
                                        input_field_view,
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
                                        train_floating_button_view,
                                        download_table_floating_button_view
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
