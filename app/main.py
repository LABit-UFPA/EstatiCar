"""
FlechaSQL — Composition Root
============================
This is the only place where concrete implementations are instantiated and
wired together (Dependency Injection).  Every other module depends only on
abstractions (ports) or on its own layer.

Layers (inner → outer):
    domain  →  infrastructure  →  presentation
"""

import flet as ft

# -- Infrastructure (concrete implementations) --------------------------------
from infrastructure.adapters.ollama_adapter import OllamaAdapter
from infrastructure.adapters.sqlite_adapter import SQLiteAdapter
from infrastructure.adapters.file_adapter import FileAdapter
from infrastructure.config.config_adapter import JsonConfigAdapter

# -- Domain (use cases) -------------------------------------------------------
from domain.use_cases.ask_question import AskQuestionUseCase
from domain.use_cases.train_model import TrainModelUseCase
from domain.use_cases.export_result import ExportResultUseCase

# -- Presentation --------------------------------------------------------------
from presentation.theme.theme_config import apply_theme
from presentation.state.app_state import AppState
from presentation.components.progress_dialog import build_progress_dialog
from presentation.components.error_dialog import ErrorDialog
from presentation.views.card_content_view import CardContentView
from presentation.views.query_content_view import QueryContentView
from presentation.views.tabs_view import TabsView
from presentation.views.input_field_view import InputFieldView
from presentation.views.footer_view import build_footer
from presentation.views.train_button_view import build_train_button
from presentation.views.download_button_view import build_download_button
from presentation.views.column_filter_view import ColumnFilterView
from presentation.controllers.question_controller import QuestionController
from presentation.controllers.training_controller import TrainingController
from presentation.controllers.download_controller import DownloadController


def main(page: ft.Page) -> None:
    try:
        # ── Theme ────────────────────────────────────────────────────────────────
        apply_theme(page)

        # ── State ────────────────────────────────────────────────────────────────
        state = AppState()

        # ── Infrastructure adapters ──────────────────────────────────────────────
        config_adapter = JsonConfigAdapter()
        ai_adapter = OllamaAdapter(model=state.choice)
        db_adapter = SQLiteAdapter()
        file_adapter = FileAdapter()

        # ── Use cases ────────────────────────────────────────────────────────
        ask_question_uc = AskQuestionUseCase(ai_model=ai_adapter, config=config_adapter)
        train_model_uc = TrainModelUseCase(
            ai_model=ai_adapter, database=db_adapter, config=config_adapter
        )
        export_result_uc = ExportResultUseCase(file_service=file_adapter)

        # ── Presentation components ──────────────────────────────────────────
        progress_dialog = build_progress_dialog()
        error_dialog = ErrorDialog(page)
        
        # Add dialogs to overlay so they can be displayed
        page.overlay.append(progress_dialog)
        page.overlay.append(error_dialog._dialog)

        card_view = CardContentView(initial_text="O Resultado será mostrado aqui...")
        card_content = card_view.build()

        query_view = QueryContentView()
        query_content = query_view.build()

        # ── Controllers ──────────────────────────────────────────────────────
        question_ctrl = QuestionController(
            page=page,
            use_case=ask_question_uc,
            state=state,
            progress_dialog=progress_dialog,
            error_dialog=error_dialog,
            card_content=card_content,
            query_content=query_content,
        )
        training_ctrl = TrainingController(
            page=page,
            use_case=train_model_uc,
            ai_adapter=ai_adapter,
            state=state,
            progress_dialog=progress_dialog,
        )
        download_ctrl = DownloadController(
            page=page, use_case=export_result_uc, state=state
        )

        # ── Views ────────────────────────────────────────────────────────────
        def on_question(e):
            question_ctrl.handle(e, input_field_view.control)

        input_field_view = InputFieldView(on_submit=on_question, page=page)

        filter_view = ColumnFilterView(
            page=page,
            state=state,
            on_train=training_ctrl.handle,
            file_port=file_adapter,
        )

        tabs = TabsView(page).build(card_content=card_content, query_content=query_content)
        train_button = build_train_button(on_click=filter_view.open)
        download_button = build_download_button(on_click=lambda e: download_ctrl.handle(e))
        footer = build_footer()

        # ── File picker (for save dialog) ────────────────────────────────────
        file_picker = ft.FilePicker(on_result=None)
        page.file_picker = file_picker
        page.add(file_picker)

        # ── Page layout ──────────────────────────────────────────────────────
        page.add(
            ft.Container(
                height=page.window.height,
                width=page.window.width,
                padding=ft.padding.all(20),
                alignment=ft.alignment.center,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                input_field_view.control,
                                ft.IconButton(
                                    icon=ft.Icons.SEARCH,
                                    on_click=on_question,
                                ),
                            ],
                        ),
                        ft.SelectionArea(tabs),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[train_button, download_button],
                        ),
                        footer,
                    ],
                ),
            )
        )
        
        # ── Update page ──────────────────────────────────────────────────────
        page.update()

    except Exception as e:
        print(f"Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        # Show error in the page
        page.clean()
        page.add(
            ft.Column([
                ft.Text(f"Erro ao inicializar aplicação:", size=20, color="red"),
                ft.Text(f"{str(e)}", size=14),
            ])
        )
        page.update()


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
