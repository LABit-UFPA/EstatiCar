from __future__ import annotations

import os
import subprocess
from typing import Any

import pandas as pd

from domain.ports.file_port import FilePort


class FileAdapter(FilePort):
    """Adapter that implements FilePort using the local file system."""

    def save_dataframe_to_excel(self, data: Any, path: str) -> None:
        data.to_excel(path, index=False)

    def open_directory(self, dir_path: str) -> None:
        if os.name == "nt":
            os.startfile(dir_path)
        else:
            subprocess.Popen(["xdg-open", dir_path])

    def read_excel(self, path: str) -> Any:
        return pd.read_excel(path)
