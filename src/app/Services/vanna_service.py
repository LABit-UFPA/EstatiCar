from vanna.remote import VannaDefault
from app.Controller.load_credentials import load_credentials

class VannaService:
    credentials_file = load_credentials()
    credentials_path_database = credentials_file[1]
    path_db_sqlite = credentials_path_database['path_db']

    def train_model_vanna_from_openia(path_db_sqlite: str, credentials_path_database: str, api_key_vanna, vanna_model_name):
        vn = VannaDefault(model=vanna_model_name, api_key=api_key_vanna)
        vn.connect_to_sqlite(path_db_sqlite)
        training_data = vn.get_training_data()

        if len(training_data.columns) != 0:
            for id_train in training_data['id']:
                training_data = vn.remove_training_data(id=id_train)
                
        vn.train(sql=f"SELECT * FROM app_data_base")