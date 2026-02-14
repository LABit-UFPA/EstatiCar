from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseCredentials:
    """Holds database connection information."""

    path_db: str
    table_db: str = "app_data_base"
