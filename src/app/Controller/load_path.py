import os
import sys


def load_path(relative_path : str):
    
    from_exe_json_path_credentials = os.path.dirname(sys.executable)
    config_path_credentials_from_exe = os.path.join(from_exe_json_path_credentials, relative_path)
    
    from_file_json_path_credentials = os.path.dirname(__file__)
    config_path_credentials_from_file = os.path.join(from_file_json_path_credentials, relative_path)

    if os.path.exists(config_path_credentials_from_exe):
        absolute_path = config_path_credentials_from_exe

    elif os.path.exists(config_path_credentials_from_file):
        absolute_path = config_path_credentials_from_file

    return absolute_path