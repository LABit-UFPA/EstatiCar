from __future__ import annotations

import flet as ft

from domain.use_cases.export_result import ExportResultUseCase
from presentation.state.app_state import AppState


class DownloadController:
    """Handles exporting the last query result to an Excel file."""

    def __init__(
        self,
        page: ft.Page,
        use_case: ExportResultUseCase,
        state: AppState,
    ) -> None:
        self._page = page
        self._use_case = use_case
        self._state = state

    def handle(self, e=None) -> None:
        if self._state.last_result is not None:

            def on_result(event):
                if event.path:
                    msg = self._use_case.execute(self._state.last_result, event.path)
                    self._page.snack_bar = ft.SnackBar(ft.Text(msg))
                    self._page.snack_bar.open = True
                    self._page.update()

            self._page.file_picker.on_result = on_result
            self._page.file_picker.save_file()
        else:
            self._page.snack_bar = ft.SnackBar(
                ft.Text("Nenhum resultado encontrado para salvar")
            )
            self._page.snack_bar.open = True
            self._page.update()
