from Controller.load_credentials import load_credentials

from Services.qdrant_client import client
from Services.ollama_service import OllamaService

class VannaService:
    credentials_path_database = load_credentials()
    path_db_sqlite = credentials_path_database['path_db']

    def train_model_vanna_from_openia(path_db_sqlite: str, model : str):
        vn = OllamaService(config={'client': client, 'model': model.lower()})
        vn.connect_to_sqlite(path_db_sqlite)
        training_data = vn.get_training_data()
        if len(training_data.columns) != 0:
            for id_train in training_data['id']:
                training_data = vn.remove_training_data(id=id_train)
        
        vn.train(sql=f"SELECT * FROM app_data_base")