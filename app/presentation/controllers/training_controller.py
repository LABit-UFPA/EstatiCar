from __future__ import annotations

import time
import logging
import flet as ft

from domain.use_cases.train_model import TrainModelUseCase
from infrastructure.adapters.ollama_adapter import OllamaAdapter
from presentation.state.app_state import AppState

logger = logging.getLogger(__name__)


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
        # Disable UI and show progress notification
        if hasattr(self._page, 'set_ui_busy'):
            self._page.set_ui_busy(True)
        if hasattr(self._page, 'show_notification'):
            self._page.show_notification("Treinando o modelo...", ft.colors.BLUE, duration=300)

        try:
            logger.info(f"Starting model training with {len(columns)} columns")
            self._ai_adapter.set_model(model)
            self._state.choice = model
            self._use_case.execute(excel_path, columns)
            logger.info("Model training completed")
        except Exception as ex:
            logger.error(f"Training failed: {ex}")
        finally:
            # Re-enable UI
            if hasattr(self._page, 'set_ui_busy'):
                self._page.set_ui_busy(False)
            # Hide processing notification
            if hasattr(self._page, 'hide_notification'):
                self._page.hide_notification()
            # Show success notification
            import time
            time.sleep(0.1)  # Small delay to ensure processing notification is hidden
            if hasattr(self._page, 'show_notification'):
                self._page.show_notification("Modelo treinado com sucesso!", ft.colors.GREEN, duration=5)
