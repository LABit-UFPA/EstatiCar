from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class DatabasePort(ABC):
    """Port for database operations (creating/importing data)."""

    @abstractmethod
    def import_excel_to_db(
        self, db_path: str, excel_path: str, columns: list[str]
    ) -> None:
        """Read an Excel file and persist selected columns to the database."""
        ...

    @abstractmethod
    def connect(self, db_path: str) -> Any:
        """Return a database connection."""
        ...
