import flet as ft
import pandas as pd
from vanna.remote import VannaDefault
from app.Components.data_table import data_table
from app.Controller.load_credentials import load_credentials

def set_question(e, page, input_field_view, progress_dialog, error_dialog_view, card_content, QueryContentView, last_result=None):
        prompt = input_field_view.value
        if prompt.strip():
            progress_dialog.open = True
            page.update()

            jsonFile = load_credentials()
            credentials = jsonFile[0]
            info_database = jsonFile[1]
            path_db_sqlite = info_database['path_db']
            api_key = credentials['api_key_vanna']
            vanna_model_name = credentials['vanna_model_name']
            
            vn = VannaDefault(model=vanna_model_name, api_key=api_key)
            vn.connect_to_sqlite(path_db_sqlite)
            result = vn.ask(prompt, visualize=False, print_results=False, allow_llm_to_see_data=True)
            last_result = result[1]
            table = data_table(result[1])

            if type(result[1]) == pd.DataFrame and not result[1].empty:
                card_content.controls = [
                    ft.Text("Resultado da pesquisa: \n"),
                    table
                ]
                QueryContentView.query_content.controls = [ft.Text("Query uilizada para a pesquisa: \n\n" + result[0]),]

                progress_dialog.open = False
                card_content.update()
                page.update()
            else:
                progress_dialog.open = False
                error_dialog_view.show_error_dialog()
