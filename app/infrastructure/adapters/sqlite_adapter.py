from __future__ import annotations

import sqlite3
from typing import Any

import pandas as pd

from domain.ports.database_port import DatabasePort


class SQLiteAdapter(DatabasePort):
    """Adapter that implements DatabasePort using SQLite."""

    def import_excel_to_db(
        self, db_path: str, excel_path: str, columns: list[str]
    ) -> None:
        con = sqlite3.connect(db_path)
        try:
            df = pd.read_excel(excel_path)
            df_filtered = df[columns]
            df_filtered.to_sql("app_data_base", con, if_exists="replace")
        finally:
            con.close()

    def connect(self, db_path: str) -> Any:
        return sqlite3.connect(db_path)
