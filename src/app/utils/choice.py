import os
import sys

def load_path(relative_path: str) -> str:
    """
    Retorna o caminho absoluto para um arquivo a partir do caminho relativo.
    Funciona tanto em execução normal quanto quando empacotado em executável.
    """

    if getattr(sys, 'frozen', False):  
        base_dir = sys._MEIPASS if hasattr(sys, "_MEIPASS") else os.path.dirname(sys.executable)
    else:
        base_dir = os.path.abspath(os.path.dirname(__file__))

    full_path = os.path.join(base_dir, "..", relative_path)
    full_path = os.path.abspath(full_path)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    return full_path


def record_choice(choice_llm):
    path_data_choice = load_path("utils/choice.txt")
    with open(path_data_choice, "w") as f:
        f.write(choice_llm)
        
def read_choice():
    path_data_choice = load_path("utils/choice.txt")
    with open(path_data_choice, "r") as f:
        choice_llm = f.read().strip()
    return choice_llm
