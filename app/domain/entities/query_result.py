from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class QueryResult:
    """Represents the result of an AI-generated SQL query execution."""

    sql: str
    data: Any  # pandas DataFrame at runtime, kept as Any to avoid domain→pandas coupling
    is_empty: bool = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "is_empty", self.data is None or len(self.data) == 0)
