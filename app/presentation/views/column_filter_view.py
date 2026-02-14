from __future__ import annotations

from typing import Callable

import flet as ft
import pandas as pd

from presentation.components.data_table import build_data_table
from presentation.components.dropdown_menu import DropdownMenu
from presentation.state.app_state import AppState

AVAILABLE_MODELS = [
    "mistral:latest",
    "llama3.1:latest",
    "gemma3:4b",
    "smollm2:1.7b",
    "qwen3:4b",
]


class ColumnFilterView:
    """Dialog for selecting Excel columns and choosing an LLM model before training."""

    def __init__(
        self,
        page: ft.Page,
        state: AppState,
        on_train: Callable[[str, list[str], str], None],
        file_port,
    ) -> None:
        self._page = page
        self._state = state
        self._on_train = on_train
        self._file_port = file_port

        self._excel_path: str | None = None
        self._df: pd.DataFrame | None = None

        self._include_list = ft.ListView(expand=True, controls=[])
        self._exclude_list = ft.ListView(expand=True, controls=[])

        self._file_picker = ft.FilePicker(on_result=self._on_file_picked)
        self._page.overlay.append(self._file_picker)

        self._model_dropdown = DropdownMenu(
            page=self._page,
            options=AVAILABLE_MODELS,
            label="Escolha o modelo de IA",
            on_change=lambda e: self._update_choice(e),
        ).control

    # -- Private helpers -----------------------------------------------------

    def _update_choice(self, e) -> None:
        self._state.choice = e.control.value

    def _on_file_picked(self, e) -> None:
        if not e.files:
            return
        self._excel_path = e.files[0].path
        self._df = self._file_port.read_excel(self._excel_path)
        self._rebuild_column_lists()
        self._page.update()

    def _rebuild_column_lists(self) -> None:
        self._exclude_list.controls.clear()
        self._include_list.controls.clear()
        if self._df is not None:
            for col in self._df.columns:
                self._exclude_list.controls.append(
                    ft.TextButton(text=col, on_click=self._toggle_item)
                )

    def _toggle_item(self, e) -> None:
        btn = e.control
        if btn in self._include_list.controls:
            self._include_list.controls.remove(btn)
            self._exclude_list.controls.append(btn)
        elif btn in self._exclude_list.controls:
            self._exclude_list.controls.remove(btn)
            self._include_list.controls.append(btn)
        self._page.update()

    def _move_to_include(self, e) -> None:
        if self._exclude_list.controls:
            item = self._exclude_list.controls.pop(0)
            self._include_list.controls.append(item)
            self._page.update()

    def _move_to_exclude(self, e) -> None:
        if self._include_list.controls:
            item = self._include_list.controls.pop(0)
            self._exclude_list.controls.append(item)
            self._page.update()

    def _move_all_to_include(self, e) -> None:
        self._include_list.controls.extend(self._exclude_list.controls[:])
        self._exclude_list.controls.clear()
        self._page.update()

    def _move_all_to_exclude(self, e) -> None:
        self._exclude_list.controls.extend(self._include_list.controls[:])
        self._include_list.controls.clear()
        self._page.update()

    def _handle_train_click(self) -> None:
        columns = [btn.text for btn in self._include_list.controls]
        model = self._model_dropdown.value
        if self._excel_path and columns:
            # Close the dialog first
            if self._page.dialog:
                self._page.dialog.open = False
                self._page.update()
            self._on_train(self._excel_path, columns, model)

    # -- Public API ----------------------------------------------------------

    def open(self) -> None:
        print("Abrindo dialog de filtro de colunas...")
        try:
            dialog = self._build()
            self._page.dialog = dialog
            dialog.open = True
            self._page.update()
            print("Dialog de filtro aberto com sucesso")
        except Exception as e:
            print(f"Erro ao abrir dialog: {e}")
            import traceback
            traceback.print_exc()

    def _build(self) -> ft.AlertDialog:
        exclude_container = ft.Container(
            content=ft.Column([
                ft.Text("Colunas Removidas:", size=16, weight=ft.FontWeight.BOLD, color="red600"),
                ft.Container(self._exclude_list, border=ft.border.all(1), padding=10, height=150),
            ]),
            border=ft.border.all(2, ft.colors.RED),
            padding=10,
            expand=1,
        )

        include_container = ft.Container(
            content=ft.Column([
                ft.Text("Colunas Selecionadas:", size=16, weight=ft.FontWeight.BOLD, color="green600"),
                ft.Container(self._include_list, border=ft.border.all(1), padding=10, height=150),
            ]),
            border=ft.border.all(2, ft.colors.GREEN),
            padding=10,
            expand=1,
        )

        buttons = ft.Column([
            ft.ElevatedButton("→", on_click=self._move_to_include),
            ft.ElevatedButton(">>", on_click=self._move_all_to_include),
            ft.ElevatedButton("<<", on_click=self._move_all_to_exclude),
            ft.ElevatedButton("←", on_click=self._move_to_exclude),
        ])

        return ft.AlertDialog(
            title=ft.Text("Filtrar Colunas", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                height=600,
                width=600,
                content=ft.Column([
                    ft.FilledButton(
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            side=ft.BorderSide(1, ft.colors.BLUE_ACCENT_100),
                            elevation=2,
                        ),
                        text="Selecionar arquivo",
                        height=50,
                        width=260,
                        on_click=lambda _: self._file_picker.pick_files(
                            allow_multiple=False, allowed_extensions=["xlsx"]
                        ),
                    ),
                    ft.Row([exclude_container, buttons, include_container]),
                    ft.Text(
                        "Escolha qual IA quer utilizar:",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                    self._model_dropdown,
                ]),
            ),
            actions=[
                ft.FilledButton(
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        side=ft.BorderSide(1, ft.colors.BLUE_ACCENT_100),
                        elevation=2,
                    ),
                    text="Realizar Treinamento",
                    height=50,
                    width=260,
                    on_click=lambda _: self._handle_train_click(),
                )
            ],
        )
