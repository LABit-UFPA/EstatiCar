import os
import sys
import json

def load_credentials():
    json_path_credentials = os.path.dirname(sys.executable)
    # json_path_credentials = os.path.dirname(__file__)
    config_path_credentials = os.path.join(json_path_credentials, r"json\credentials.json")

    with open(config_path_credentials, 'r') as config_file:
        config_data_credentials = json.load(config_file)

    data_base_path = os.path.dirname(sys.executable)
    # data_base_path = os.path.dirname(__file__)
    path_db_sqlite = os.path.join(data_base_path, r"DB\app_data_base.db")

    json_path_database = os.path.dirname(sys.executable)
    # json_path_database = os.path.dirname(__file__)
    config_path_database = os.path.join(json_path_database, r"json\databasepath.json")
    
    with open(config_path_database, 'r') as config_file:
        config_data_path_database = json.load(config_file)

    if path_db_sqlite:
        config_data_path_database['path_db'] = path_db_sqlite
        with open(config_path_database, 'w') as config_file:
            json.dump(config_data_path_database, config_file, indent=4)
    else:
        print("Path não foi alterado.")
    print([config_data_credentials, config_data_path_database])
    return [config_data_credentials, config_data_path_database]
