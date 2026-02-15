from __future__ import annotations

import os
from typing import Any

from vanna.ollama import Ollama
from vanna.qdrant import Qdrant_VectorStore
from qdrant_client import QdrantClient

from domain.entities.query_result import QueryResult
from domain.ports.ai_model_port import AIModelPort


class _OllamaQdrant(Qdrant_VectorStore, Ollama):
    """Concrete Vanna class combining Qdrant vector store with Ollama LLM."""

    def __init__(self, config: dict | None = None) -> None:
        Qdrant_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)


class OllamaAdapter(AIModelPort):
    """Adapter that implements AIModelPort using Ollama + Qdrant."""

    def __init__(
        self, 
        model: str, 
        qdrant_url: str = "http://localhost:6333",
        ollama_host: str | None = None
    ) -> None:
        self._model = model
        self._ollama_host = ollama_host or os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self._client = QdrantClient(url=qdrant_url)
        self._vn: _OllamaQdrant | None = None
        self._ensure_instance()

    def _ensure_instance(self) -> None:
        config = {
            "client": self._client, 
            "model": self._model,
            "ollama_host": self._ollama_host
        }
        self._vn = _OllamaQdrant(config=config)

    def set_model(self, model: str) -> None:
        """Switch to a different LLM model."""
        self._model = model
        self._ensure_instance()

    # -- AIModelPort implementation ------------------------------------------

    def connect(self, db_path: str) -> None:
        self._vn.connect_to_sqlite(db_path)

    def ask(self, prompt: str) -> QueryResult:
        result = self._vn.ask(
            prompt, visualize=False, print_results=False, allow_llm_to_see_data=True
        )
        sql = result[0] if result[0] else ""
        data = result[1]
        return QueryResult(sql=sql, data=data)

    def train(self, sql: str) -> None:
        self._vn.train(sql=sql)

    def get_training_data(self) -> Any:
        return self._vn.get_training_data()

    def remove_training_data(self, id: str) -> None:
        self._vn.remove_training_data(id=id)
