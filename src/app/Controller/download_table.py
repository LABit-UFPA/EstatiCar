import os
import flet as ft
import pandas as pd

def download_table(page, last_result):
    if last_result is not None:
        def on_result(e):
            if e.path:
                try:
                    save_path = f"{e.path}.xlsx"
                    last_result.to_excel(save_path, index=False)

                    if os.name == 'nt':  # Se for Windows, tenta abrir o diretório
                        os.startfile(os.path.dirname(save_path))

                    msg = "Tabela salva com sucesso."
                except Exception as ex:
                    msg = f"Erro ao salvar: {ex}"

                snack_bar = ft.SnackBar(ft.Text(msg))
                snack_bar.open = True
                page.update()

        page.file_picker.on_result = on_result
        page.file_picker.save_file()
    else:
        snack_bar = ft.SnackBar(ft.Text("Nenhum resultado encontrado para salvar"))
        snack_bar.open = True
        page.update()