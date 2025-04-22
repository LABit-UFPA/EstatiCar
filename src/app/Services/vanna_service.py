from vanna.remote import VannaDefault
from vanna.anthropic.anthropic_chat import Anthropic_Chat
from vanna.vannadb.vannadb_vector import VannaDB_VectorStore
from app.Controller.load_credentials import load_credentials

class VannaService:
    credentials_file = load_credentials()
    credentials_path_database = credentials_file[1]
    path_db_sqlite = credentials_path_database['path_db']

    def train_model_vanna_from_openia(path_db_sqlite: str, api_key_vanna, vanna_model_name):
        vn = VannaDefault(model=vanna_model_name, api_key=api_key_vanna)
        vn.connect_to_sqlite(path_db_sqlite)
        training_data = vn.get_training_data()

        if len(training_data.columns) != 0:
            for id_train in training_data['id']:
                training_data = vn.remove_training_data(id=id_train)
                
        vn.train(sql=f"SELECT * FROM app_data_base")
    
    def train_model_claude(path_db_sqlite: str, api_key_claude, api_key_vanna, vanna_model_name):
        api_key = api_key_claude
        model = "claude-3.5-sonnet-20240620"
        config = {'api_key':api_key,'model':model}
        
        class MyVanna(VannaDB_VectorStore, Anthropic_Chat):
            def __init__(self, config=None):
                MY_VANNA_MODEL =  vanna_model_name
                VannaDB_VectorStore.__init__(self, vanna_model=MY_VANNA_MODEL, vanna_api_key= api_key_vanna, config=config)
                Anthropic_Chat.__init__(self, config=config)

        vn = MyVanna(config=config)
        
        vn.connect_to_sqlite(path_db_sqlite)
        
        training_data = vn.get_training_data()

        if len(training_data.columns) != 0:
            for id_train in training_data['id']:
                training_data = vn.remove_training_data(id=id_train)
                
        vn.train(sql=f"SELECT * FROM app_data_base")