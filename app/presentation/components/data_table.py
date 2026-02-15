from __future__ import annotations

import flet as ft
import pandas as pd


def build_data_table(df: pd.DataFrame | None) -> ft.DataTable:
    """Build a modern Flet DataTable from a pandas DataFrame."""
    if df is None or df.empty:
        df = pd.DataFrame(columns=["No Data"])

    columns = [
        ft.DataColumn(
            ft.Text(
                col.replace("_", " ").title(),
                weight=ft.FontWeight.W_600,
                size=16,
                color="#475569",
            )
        )
        for col in df.columns
    ]
    rows = []
    for idx, row in df.iterrows():
        cells = [
            ft.DataCell(
                ft.Text(
                    str(value),
                    size=15,
                    color="#1e293b",
                )
            )
            for value in row
        ]
        # Alternate row colors for better readability
        rows.append(
            ft.DataRow(
                cells=cells,
                color=ft.colors.TRANSPARENT if idx % 2 == 0 else "#f8fafc",
            )
        )

    return ft.DataTable(
        columns=columns,
        rows=rows,
        border=ft.border.all(1, "#e2e8f0"),
        border_radius=12,
        heading_row_color="#f1f5f9",
        heading_row_height=56,
        data_row_min_height=52,
        data_row_max_height=72,
        column_spacing=32,
        horizontal_margin=24,
        show_checkbox_column=False,
    )
