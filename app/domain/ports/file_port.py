from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class FilePort(ABC):
    """Port for file system operations."""

    @abstractmethod
    def save_dataframe_to_excel(self, data: Any, path: str) -> None:
        """Persist a DataFrame to an Excel file."""
        ...

    @abstractmethod
    def open_directory(self, dir_path: str) -> None:
        """Open a directory in the OS file explorer."""
        ...

    @abstractmethod
    def read_excel(self, path: str) -> Any:
        """Read an Excel file and return a DataFrame."""
        ...
