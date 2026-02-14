from __future__ import annotations

import os
from typing import Any

from domain.ports.file_port import FilePort


class ExportResultUseCase:
    """Exports a query result (DataFrame) to an Excel file."""

    def __init__(self, file_service: FilePort) -> None:
        self._file_service = file_service

    def execute(self, data: Any, save_path: str) -> str:
        """Save *data* to *save_path* and open the containing folder.

        Returns a user-facing status message.
        """
        try:
            full_path = f"{save_path}.xlsx"
            self._file_service.save_dataframe_to_excel(data, full_path)
            self._file_service.open_directory(os.path.dirname(full_path))
            return "Tabela salva com sucesso."
        except Exception as ex:
            return f"Erro ao salvar: {ex}"
