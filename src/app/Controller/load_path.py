import os
import sys


def load_path_credentials():
    from_exe_json_path_credentials = os.path.dirname(sys.executable)
    config_path_credentials_from_exe = os.path.join(from_exe_json_path_credentials, r"json\credentials.json")
    
    from_file_json_path_credentials = os.path.dirname(__file__)
    config_path_credentials_from_file = os.path.join(from_file_json_path_credentials, r"json\credentials.json")
    
    if os.path.exists(config_path_credentials_from_exe):
        path_credentials = config_path_credentials_from_exe

    elif os.path.exists(config_path_credentials_from_file):
        path_credentials = config_path_credentials_from_file

    return path_credentials

def load_path_config_database():
    from_exe_json_path_database = os.path.dirname(sys.executable)
    config_path_database_from_exe = os.path.join(from_exe_json_path_database, r"json\databasepath.json")
    
    from_file_json_path_database = os.path.dirname(__file__)
    config_path_database_from_file = os.path.join(from_file_json_path_database, r"json\databasepath.json")
    
    if os.path.exists(config_path_database_from_exe):
        path_database = config_path_database_from_exe

    elif os.path.exists(config_path_database_from_file):
        path_database = config_path_database_from_file

    return path_database

def load_path_sqlite_database():
    from_exe_json_path_sqlite_database = os.path.dirname(sys.executable)
    config_path_sqlite_database_from_exe = os.path.join(from_exe_json_path_sqlite_database, r"DB\app_data_base.db")
    
    from_file_json_path_sqlite_database = os.path.dirname(__file__)
    config_path_sqlite_database_from_file = os.path.join(from_file_json_path_sqlite_database, r"DB\app_data_base.db")
    
    if os.path.exists(config_path_sqlite_database_from_exe):
        path_sqlite_database = config_path_sqlite_database_from_exe

    elif os.path.exists(config_path_sqlite_database_from_file):
        path_sqlite_database = config_path_sqlite_database_from_file

    return path_sqlite_database

