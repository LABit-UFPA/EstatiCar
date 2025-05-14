import flet as ft

from app.Themes.themes_data import ThemeData

from app.View.tabs_view import TabsView
from app.View.footer_view import FooterView
from app.View.input_field_view import InputFieldView
from app.View.card_content_view import CardContentView
from app.View.query_content_view import QueryContentView
from app.View.column_filter_view import ColumnFilterDialog
from app.View.train_button import TrainButtonView
from app.View.download_table_button import DownloadTableButtonView

from app.Components.progress_dialog import ProgressDialog
from app.Components.errors_app import ErrorApp

from app.Controller.set_question import set_question
from app.Controller.download_table import download_table

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

    exec_set_question = lambda e: set_question(e, page, input_field_view, progress_dialog, error_dialog_view, card_content, QueryContentView, last_result)

    train_floating_button_view = TrainButtonView(page, filter_dialog_view.open).train_button_view()

    download_table_floating_button = DownloadTableButtonView(event_handler=lambda e: download_table(page, last_result))
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
                                            on_click=exec_set_question(lambda e: exec_set_question(e)),
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
