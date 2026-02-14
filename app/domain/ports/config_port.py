from __future__ import annotations

from abc import ABC, abstractmethod

from domain.entities.credentials import DatabaseCredentials


class ConfigPort(ABC):
    """Port for loading application configuration."""

    @abstractmethod
    def load_credentials(self) -> DatabaseCredentials:
        """Load and return database credentials."""
        ...
