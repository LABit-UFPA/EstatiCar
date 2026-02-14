from __future__ import annotations

from domain.ports.ai_model_port import AIModelPort
from domain.ports.config_port import ConfigPort
from domain.ports.database_port import DatabasePort


class TrainModelUseCase:
    """Imports an Excel file into the database and trains the AI model."""

    def __init__(
        self,
        ai_model: AIModelPort,
        database: DatabasePort,
        config: ConfigPort,
    ) -> None:
        self._ai_model = ai_model
        self._database = database
        self._config = config

    def execute(self, excel_path: str, columns: list[str]) -> None:
        credentials = self._config.load_credentials()

        # 1. Import selected columns into the SQLite database
        self._database.import_excel_to_db(
            db_path=credentials.path_db,
            excel_path=excel_path,
            columns=columns,
        )

        # 2. Clear old training data
        training_data = self._ai_model.get_training_data()
        if len(training_data.columns) != 0:
            for id_train in training_data["id"]:
                self._ai_model.remove_training_data(id=id_train)

        # 3. Connect and train on all rows
        self._ai_model.connect(credentials.path_db)
        self._ai_model.train(sql="SELECT * FROM app_data_base")
