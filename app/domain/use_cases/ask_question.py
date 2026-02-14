from __future__ import annotations

from domain.entities.query_result import QueryResult
from domain.ports.ai_model_port import AIModelPort
from domain.ports.config_port import ConfigPort


class AskQuestionUseCase:
    """Sends a natural-language question to the AI model and returns the query result."""

    def __init__(self, ai_model: AIModelPort, config: ConfigPort) -> None:
        self._ai_model = ai_model
        self._config = config

    def execute(self, prompt: str) -> QueryResult:
        credentials = self._config.load_credentials()
        self._ai_model.connect(credentials.path_db)
        return self._ai_model.ask(prompt)
