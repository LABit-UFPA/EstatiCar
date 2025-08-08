import os
import sys
import json
import flet as ft
import pandas as pd
from Components.data_table import data_table
from concurrent.futures import ThreadPoolExecutor
from Services.vanna_service import VannaService
from Services.database_config import DatabaseConfig
from Components.progress_dialog import ProgressDialog
from Controller.load_path import load_path

class TimeoutException(Exception):
    """Exception raised when a function call times out."""
    pass

class ProcessDataTable:
    def __init__(self, page):
        self.page = page
        self.df = None
        self.page.dialog = ProgressDialog.progress_dialog
        self.file_picker = ft.FilePicker(on_result=self.view_preprocess_df)
        self.page.overlay.append(self.file_picker)
        self.page.add(self.file_picker)

        self.excel_path = None
        self.items = []
        self.include_list = ft.ListView(expand=True, controls=[])
        self.exclude_list = ft.ListView(expand=True, controls=[])
        self.build_lists(self.items)

    def resetLists(self):
        self.exclude_list.controls = []
        self.include_list.controls = []

    def pre_process_df(self):
        if self.df is None or self.df.empty:
            self.df = pd.DataFrame(columns=["No Data"])
        return self.df

    def on_file_picked(self, e):
        if e.files:    
            ProgressDialog.progress_dialog.open = True
            self.page.update()
            self.excel_path = e.files[0].path
            ProgressDialog.progress_dialog.open = False
            self.page.update()
            
            return self.excel_path

    def view_preprocess_df(self, e):
        self.excel_path = self.on_file_picked(e)
        self.df = pd.read_excel(self.excel_path)
        self.process_table_config = self.pre_process_df()
        self.items = self.get_columns()
        self.build_lists(self.items)
        self.page.update()
 
    def init_process_files(self, choice_llm):

        ProgressDialog.progress_dialog.open = True
        self.page.update()

        def process_files():
            try:
                name_columns_include = [button.text for button in self.include_list.controls]
                DatabaseConfig.create_db(DatabaseConfig.credentials_path_database, DatabaseConfig.path_db_sqlite, self.excel_path, name_columns_include)

                if choice_llm == "Mistral":
                    def train_vanna_with_timeout(choice = "Mistral"):
                        try:
                            VannaService.train_model_vanna_from_openia(VannaService.path_db_sqlite, choice)
                        except Exception as e:
                            print(f"Vanna training error: {e}")
                            raise

                    with ThreadPoolExecutor() as executor:
                        future = executor.submit(train_vanna_with_timeout)
                        try:
                            future.result(timeout=20)
                        except TimeoutError:
                            print("Vanna model training timed out after 20 seconds")
                            self.page.snack_bar = ft.SnackBar(
                                ft.Text("Treinamento do modelo Vanna excedeu o tempo limite de 20 segundos!")
                            )
                            self.page.snack_bar.open = True
                            return
                elif choice_llm == "llama":
                    def train_vanna_with_timeout(choice = "llama"):
                        try:
                            VannaService.train_model_vanna_from_openia(VannaService.path_db_sqlite, choice)
                        except Exception as e:
                            print(f"Vanna training error: {e}")
                            raise

                    with ThreadPoolExecutor() as executor:
                        future = executor.submit(train_vanna_with_timeout)
                        try:
                            future.result(timeout=20)
                        except TimeoutError:
                            print("Vanna model training timed out after 20 seconds")
                            self.page.snack_bar = ft.SnackBar(
                                ft.Text("Treinamento do modelo Vanna excedeu o tempo limite de 20 segundos!")
                            )
                            self.page.snack_bar.open = True
                            return
                        
                ProgressDialog.progress_dialog.open = False
                self.page.snack_bar = ft.SnackBar(ft.Text("Modelo treinado com sucesso!"))
                self.page.snack_bar.open = True
                self.page.update()

            except Exception as e:
                print(f"Error in process_files: {e}")
                ProgressDialog.progress_dialog.open = False
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Erro no processamento: {str(e)}"))
                self.page.snack_bar.open = True
                self.page.update()

        with ThreadPoolExecutor() as executor:
            executor.submit(process_files)

    def build_lists(self, items):
        if self.excel_path is None:
            for item in items:
                self.exclude_list.controls.append(
                    ft.TextButton(text=item, on_click=self.toggle_item)
                )
        if self.excel_path is not None:
            columns = self.get_columns()
            for column in columns:
                self.exclude_list.controls.append(ft.TextButton(text=column, on_click=self.toggle_item))

    def move_to_exclude(self, e):
        if self.include_list.controls:
            item = self.include_list.controls.pop(0)
            self.exclude_list.controls.append(item)
            self.page.update()
    
    def move_to_include(self, e):
        if self.exclude_list.controls:
            item = self.exclude_list.controls.pop(0)
            self.include_list.controls.append(item)
            self.page.update()

    
    def toggle_item(self, e):
        btn = e.control
        if btn in self.include_list.controls:
            self.include_list.controls.remove(btn)
            self.exclude_list.controls.append(btn)
        elif btn in self.exclude_list.controls:
            self.exclude_list.controls.remove(btn)
            self.include_list.controls.append(btn)
        self.page.update()
        
    def get_df(self):
        self.df = data_table(self.df)
        return self.df

    def get_columns(self):
        return self.df.columns
    
    def get_rows(self):
        return self.df.iterrows()
    
    def get_exclude_list(self):
        return self.exclude_list
    
    def get_include_list(self):
        return self.include_list
        

    # checar viabilidade de usar o metodo abaixo
    def get_field_rows(self, df):
        rows = []
        for _, row in df.iterrows():
            cells = [ft.DataCell(ft.Text(str(value))) for value in row]
            rows.append(ft.DataRow(cells=cells))
        return rows

    def get_field_columns(self):
        columns = [ft.DataColumn(ft.Text(col.replace("_", " ").title())) for col in self.df.columns]
        return columns