from __future__ import annotations

import time
import logging
import flet as ft
import pandas as pd

from domain.use_cases.ask_question import AskQuestionUseCase
from presentation.components.data_table import build_data_table
from presentation.state.app_state import AppState

logger = logging.getLogger(__name__)


class QuestionController:
    """Handles the 'ask a question' flow between the UI and the use case."""

    def __init__(
        self,
        page: ft.Page,
        use_case: AskQuestionUseCase,
        state: AppState,
        progress_dialog: ft.AlertDialog,
        error_dialog,
        card_content: ft.Column,
        query_content: ft.Column,
    ) -> None:
        self._page = page
        self._use_case = use_case
        self._state = state
        self._progress = progress_dialog
        self._error = error_dialog
        self._card_content = card_content
        self._query_content = query_content

    def handle(self, e, input_field: ft.TextField) -> None:
        prompt = input_field.value
        if not prompt or not prompt.strip():
            return

        # Disable UI and show progress notification
        if hasattr(self._page, 'set_ui_busy'):
            self._page.set_ui_busy(True)
        if hasattr(self._page, 'show_notification'):
            self._page.show_notification("Processando sua pergunta...", ft.colors.BLUE, duration=300)

        result_data = None
        show_error = False
        try:
            logger.info(f"Executing question: {prompt}")
            result = self._use_case.execute(prompt)
            self._state.last_result = result.data

            if not result.is_empty and isinstance(result.data, pd.DataFrame):
                result_data = result
            else:
                logger.warning("Empty result received")
                show_error = True
        except Exception as ex:
            logger.error(f"Question handler failed: {ex}")
            import traceback
            traceback.print_exc()
            show_error = True
        finally:
            # Re-enable UI and hide notification
            if hasattr(self._page, 'set_ui_busy'):
                self._page.set_ui_busy(False)
            if hasattr(self._page, 'hide_notification'):
                self._page.hide_notification()
            
            if result_data:
                table = build_data_table(result_data.data)
                self._card_content.controls = [
                    ft.Container(
                        content=ft.Text(
                            "Resultado da pesquisa:",
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color="#475569",
                        ),
                        margin=ft.margin.only(bottom=12),
                    ),
                    table,
                ]
                self._query_content.controls = [
                    ft.Container(
                        content=ft.Text(
                            "Query utilizada para a pesquisa:",
                            size=16,
                            weight=ft.FontWeight.W_600,
                            color="#475569",
                        ),
                        margin=ft.margin.only(bottom=12),
                    ),
                    ft.Container(
                        content=ft.Text(
                            result_data.sql,
                            size=14,
                            color="#1e293b",
                            font_family="Courier New",
                            selectable=True,
                        ),
                        bgcolor="#f8fafc",
                        border=ft.border.all(1, "#e2e8f0"),
                        border_radius=12,
                        padding=ft.padding.all(20),
                    ),
                ]
                self._card_content.update()
                self._page.update()
            elif show_error:
                self._error.show()
