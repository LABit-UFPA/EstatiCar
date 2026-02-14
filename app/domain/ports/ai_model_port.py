from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from domain.entities.query_result import QueryResult


class AIModelPort(ABC):
    """Port for interacting with AI language models."""

    @abstractmethod
    def connect(self, db_path: str) -> None:
        """Connect the AI model to a SQLite database."""
        ...

    @abstractmethod
    def ask(self, prompt: str) -> QueryResult:
        """Send a natural-language question and receive a QueryResult."""
        ...

    @abstractmethod
    def train(self, sql: str) -> None:
        """Train the model with the given SQL statement."""
        ...

    @abstractmethod
    def get_training_data(self) -> Any:
        """Return the current training data."""
        ...

    @abstractmethod
    def remove_training_data(self, id: str) -> None:
        """Remove a specific training data entry."""
        ...
