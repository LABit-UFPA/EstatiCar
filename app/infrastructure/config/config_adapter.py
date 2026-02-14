from __future__ import annotations

import json

from domain.entities.credentials import DatabaseCredentials
from domain.ports.config_port import ConfigPort
from infrastructure.config.path_resolver import resolve_path


class JsonConfigAdapter(ConfigPort):
    """Adapter that loads credentials from a JSON file on disk."""

    def __init__(
        self,
        json_relative_path: str = "json/databasepath.json",
        db_relative_path: str = "db/app_data_base.db",
    ) -> None:
        self._json_rel = json_relative_path
        self._db_rel = db_relative_path

    def load_credentials(self) -> DatabaseCredentials:
        config_path = resolve_path(self._json_rel)
        
        # Try to resolve db_path, but don't fail if it doesn't exist yet
        try:
            db_path = resolve_path(self._db_rel)
        except FileNotFoundError:
            # Database doesn't exist yet - use a default path relative to config
            import os
            config_dir = os.path.dirname(config_path)
            db_path = os.path.join(config_dir, self._db_rel)
            # Ensure the db directory exists
            os.makedirs(os.path.dirname(db_path), exist_ok=True)

        with open(config_path, "r") as f:
            data = json.load(f)

        # Update the stored db path if the resolved path differs
        if db_path and data.get("path_db") != db_path:
            data["path_db"] = db_path
            with open(config_path, "w") as f:
                json.dump(data, f, indent=4)

        return DatabaseCredentials(
            path_db=data["path_db"],
            table_db=data.get("table_db", "app_data_base"),
        )
