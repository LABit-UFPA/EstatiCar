import json
from app.Controller.load_path import load_path_credentials, load_path_config_database, load_path_sqlite_database

def load_credentials():

    config_path_credentials = load_path_credentials()
    config_path_database = load_path_config_database()
    config_path_sqlite_database = load_path_sqlite_database()

    with open(config_path_credentials, 'r') as config_file_credentials:
        config_data_credentials = json.load(config_file_credentials)

    with open(config_path_database, 'r') as config_file_database:
        config_data_path_database = json.load(config_file_database)

    if config_path_sqlite_database:
        config_data_path_database['path_db'] = config_path_sqlite_database
        with open(config_path_database, 'w') as config_file:
            json.dump(config_data_path_database, config_file, indent=4)
    else:
        print("Path não foi alterado.")
    print([config_data_credentials, config_data_path_database])
    return [config_data_credentials, config_data_path_database]
