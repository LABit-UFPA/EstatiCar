import flet as ft
from Controller.save_excel import save_excel

def download_table(page, last_result):
    if last_result is not None:
        def on_result(e, last_result):
            if e.path:
                msg = save_excel(e, last_result)
                snack_bar = ft.SnackBar(ft.Text(msg))
                snack_bar.open = True
                page.update()

        page.file_picker.on_result = on_result
        page.file_picker.save_file()
    else:
        snack_bar = ft.SnackBar(ft.Text("Nenhum resultado encontrado para salvar"))
        snack_bar.open = True
        page.update()