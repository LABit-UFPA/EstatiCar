from __future__ import annotations

import time
import flet as ft
import pandas as pd

from domain.use_cases.ask_question import AskQuestionUseCase
from presentation.components.data_table import build_data_table
from presentation.state.app_state import AppState


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
        print("[PROCESSING] Showing question progress notification...")
        if hasattr(self._page, 'set_ui_busy'):
            self._page.set_ui_busy(True)
        if hasattr(self._page, 'show_notification'):
            self._page.show_notification("⏳ Processando sua pergunta...", ft.colors.BLUE, duration=300)

        result_data = None
        show_error = False
        try:
            print(f"[PROCESSING] Executing question: {prompt}")
            result = self._use_case.execute(prompt)
            self._state.last_result = result.data
            print(f"[SUCCESS] Result received, is_empty: {result.is_empty}")

            if not result.is_empty and isinstance(result.data, pd.DataFrame):
                result_data = result
            else:
                print("[ERROR] Empty result, showing error")
                show_error = True
        except Exception as ex:
            print(f"[ERROR] Question handler failed: {ex}")
            import traceback
            traceback.print_exc()
            show_error = True
        finally:
            # Re-enable UI and hide notification
            print("[PROCESSING] Finalizing question processing...")
            if hasattr(self._page, 'set_ui_busy'):
                self._page.set_ui_busy(False)
            if hasattr(self._page, 'hide_notification'):
                self._page.hide_notification()
            
            if result_data:
                table = build_data_table(result_data.data)
                self._card_content.controls = [
                    ft.Text("Resultado da pesquisa: \n"),
                    table,
                ]
                self._query_content.controls = [
                    ft.Text("Query utilizada para a pesquisa: \n\n" + result_data.sql),
                ]
                self._card_content.update()
                self._page.update()
                print("[SUCCESS] Page updated successfully")
            elif show_error:
                self._error.show()
                print("[ERROR] Error dialog shown")
