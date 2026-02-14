from __future__ import annotations

from domain.ports.ai_model_port import AIModelPort


class DeleteTrainingDataUseCase:
    """Removes all training data from the AI model."""

    def __init__(self, ai_model: AIModelPort) -> None:
        self._ai_model = ai_model

    def execute(self) -> None:
        training_data = self._ai_model.get_training_data()
        if len(training_data.columns) != 0:
            for id_train in training_data["id"]:
                self._ai_model.remove_training_data(id=id_train)
