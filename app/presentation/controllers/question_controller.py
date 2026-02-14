from __future__ import annotations

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

        # Show progress dialog
        self._page.dialog = self._progress
        self._progress.open = True
        self._page.update()

        result_data = None
        show_error = False
        try:
            print(f"Executando pergunta: {prompt}")
            result = self._use_case.execute(prompt)
            self._state.last_result = result.data
            print(f"Resultado recebido, is_empty: {result.is_empty}")

            if not result.is_empty and isinstance(result.data, pd.DataFrame):
                result_data = result
            else:
                print("Resultado vazio, mostrando erro")
                show_error = True
        except Exception as ex:
            print(f"Error in question handler: {ex}")
            import traceback
            traceback.print_exc()
            show_error = True
        finally:
            # Always close dialog
            print("Fechando progress dialog da pergunta...")
            self._progress.open = False
            self._page.dialog = None
            
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
                print("Page atualizada com sucesso")
            elif show_error:
                self._page.update()
                self._error.show()
