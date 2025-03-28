import flet as ft
import pandas as pd

def data_table(df):

    if df is None or df.empty:
        df = pd.DataFrame(columns=["No Data"])

    columns = [ft.DataColumn(ft.Text(col.replace("_", " ").title())) for col in df.columns]
    rows = []
    
    for _, row in df.iterrows():
        cells = [ft.DataCell(ft.Text(str(value))) for value in row]
        rows.append(ft.DataRow(cells=cells))
    
    return ft.DataTable(columns=columns, rows=rows)