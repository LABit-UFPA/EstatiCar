from __future__ import annotations

import flet as ft

from domain.use_cases.train_model import TrainModelUseCase
from infrastructure.adapters.ollama_adapter import OllamaAdapter
from presentation.state.app_state import AppState


class TrainingController:
    """Handles the training workflow between the UI and the use case."""

    def __init__(
        self,
        page: ft.Page,
        use_case: TrainModelUseCase,
        ai_adapter: OllamaAdapter,
        state: AppState,
        progress_dialog: ft.AlertDialog,
    ) -> None:
        self._page = page
        self._use_case = use_case
        self._ai_adapter = ai_adapter
        self._state = state
        self._progress = progress_dialog

    def handle(self, excel_path: str, columns: list[str], model: str) -> None:
        self._page.dialog = self._progress
        self._progress.open = True
        self._page.update()

        try:
            self._ai_adapter.set_model(model)
            self._state.choice = model
            self._use_case.execute(excel_path, columns)
        except Exception as ex:
            print(f"Error in training: {ex}")
        finally:
            self._progress.open = False
            self._page.dialog = None
            self._page.snack_bar = ft.SnackBar(ft.Text("Modelo treinado com sucesso!"))
            self._page.snack_bar.open = True
            self._page.update()
