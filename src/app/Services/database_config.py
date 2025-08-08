import sqlite3
import pandas as pd
from app.Controller.load_credentials import load_credentials

class DatabaseConfig:
    credentials_path_database = load_credentials()
    path_db_sqlite = credentials_path_database['path_db']
    
    def __init__(self, path_file_excel: str, columns_df : list[str]):
        self.path_file_excel = path_file_excel
        self.columns_df = columns_df

    def create_db(credentials_path_database, path_db_sqlite: str, path_file_excel: str, columns_df : list[str]):
        con = sqlite3.connect(path_db_sqlite)

        df_unprocessed = pd.read_excel(path_file_excel)

        df_processed = df_unprocessed[columns_df]

        df_processed.to_sql('app_data_base', con, if_exists='replace')

