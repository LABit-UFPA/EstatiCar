import json
from Controller.load_path import load_path

def load_credentials():
    config_path_database = load_path("json/databasepath.json")  
    config_path_sqlite_database = load_path("db/app_data_base.db")

    with open(config_path_database, 'r') as config_file_database:
        config_data_path_database = json.load(config_file_database)

    if config_path_sqlite_database:
        config_data_path_database['path_db'] = config_path_sqlite_database
        with open(config_path_database, 'w') as config_file:
            json.dump(config_data_path_database, config_file, indent=4)
    else:
        print("Path não foi alterado.")
    
    return config_data_path_database
