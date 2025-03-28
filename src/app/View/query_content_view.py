import flet as ft

class QueryContentView:
    def __init__(self):
        pass    
    query_content = ft.Column(
        controls=[ft.Text(value="A query para a consulta será mostrada aqui...")],
    )