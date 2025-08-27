import flet as ft

from Themes.themes_data import ThemeData

from View.tabs_view import TabsView
from View.footer_view import FooterView
from View.input_field_view import InputFieldView
from View.card_content_view import CardContentView
from View.query_content_view import QueryContentView
from View.column_filter_view import ColumnFilterDialog
from View.train_button import TrainButtonView
from View.download_table_button import DownloadTableButtonView

from Components.progress_dialog import ProgressDialog
from Components.errors_app import ErrorApp

from Controller.set_question import set_question
from Controller.download_table import download_table

from utils import choice

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
    data_choice = choice.read_choice()
    print("\n\n\n" + data_choice + "\n\n\n")
    exec_set_question = lambda e: set_question(e, page, input_field_view, progress_dialog, error_dialog_view, card_content, QueryContentView, data_choice, last_result)

    input_field = InputFieldView(exec_set_question, page)
    input_field_view = input_field.input_field_view()

    train_floating_button_view = TrainButtonView(page, filter_dialog_view.open).train_button_view()

    download_table_floating_button = DownloadTableButtonView(event_handler=lambda e: download_table(page, last_result))
    # download_table_floating_button = DownloadTableButtonView(
    #     event_handler=lambda e: asyncio.create_task(download_table(page, last_result))
    # )

    download_table_floating_button_view = download_table_floating_button.download_table_view()

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
                                            on_click=lambda e: exec_set_question(e),
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
