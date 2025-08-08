import os
import subprocess
import pandas as pd

def save_excel(e, last_result):
    try:
        save_path = f"{e.path}.xlsx"
        last_result.to_excel(save_path, index=False)
        dir_path = os.path.dirname(save_path)
        if os.name == 'nt':  # Windows
            os.startfile(dir_path)
        else:  # Linux
            subprocess.Popen(["xdg-open", dir_path])

        msg = "Tabela salva com sucesso."
    except Exception as ex:
        msg = f"Erro ao salvar: {ex}"
    
    return msg