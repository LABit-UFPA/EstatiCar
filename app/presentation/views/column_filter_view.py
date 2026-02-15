from __future__ import annotations

import os
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
    "gemma3:27b"
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
        self._is_modal_open = False  # Flag to prevent multiple opens

        self._include_list = ft.ListView(expand=True, controls=[])
        self._exclude_list = ft.ListView(expand=True, controls=[])

        self._file_picker = ft.FilePicker(
            on_result=self._on_file_picked,
            on_upload=self._on_upload_complete
        )
        # Only add FilePicker if not already in overlay
        if self._file_picker not in self._page.overlay:
            self._page.overlay.append(self._file_picker)
        
        # Create upload directory (needed for web mode)
        self._upload_dir = os.path.join(os.getcwd(), "uploads")
        os.makedirs(self._upload_dir, exist_ok=True)
        
        # Create modal overlay container (will be shown/hidden)
        self._modal_container = ft.Container(
            visible=False,
            content=None  # Initialize with no content
        )
        # Only add modal container if not already in overlay
        if self._modal_container not in self._page.overlay:
            self._page.overlay.append(self._modal_container)
        
        self._page.update()

        self._model_dropdown = DropdownMenu(
            page=self._page,
            options=AVAILABLE_MODELS,
            label="Escolha o modelo de IA",
            on_change=lambda e: self._update_choice(e),
        ).control

    # -- Private helpers -----------------------------------------------------

    def _update_choice(self, e) -> None:
        self._state.choice = e.control.value

    def _on_file_picked(self, e: ft.FilePickerResultEvent) -> None:
        if not e.files:
            print("Nenhum arquivo selecionado")
            return
        
        try:
            # Get the selected file
            selected_file = e.files[0]
            print(f"Arquivo selecionado: {selected_file.name}")
            
            # Check if we have direct file access (desktop mode)
            if selected_file.path:
                # Desktop mode - direct file access
                self._excel_path = selected_file.path
                print(f"Arquivo com caminho direto: {self._excel_path}")
                # Read the Excel file immediately
                self._df = self._file_port.read_excel(self._excel_path)
                self._rebuild_column_lists()
                self._page.update()
                print("Arquivo carregado com sucesso")
                
                # Show success message
                if hasattr(self._page, 'show_notification'):
                    self._page.show_notification(f"✅ Arquivo '{selected_file.name}' carregado!", ft.colors.GREEN)
            else:
                # Web mode - upload file
                print("Modo web - iniciando upload...")
                self._excel_path = os.path.join(self._upload_dir, selected_file.name)
                
                # Start upload
                try:
                    upload_url = self._page.get_upload_url(selected_file.name, 600)
                    print(f"Upload URL obtida: {upload_url}")
                    self._file_picker.upload(
                        files=[ft.FilePickerUploadFile(
                            name=selected_file.name,
                            upload_url=upload_url
                        )]
                    )
                    print("Upload iniciado com sucesso")
                except Exception as upload_ex:
                    print(f"Erro ao iniciar upload: {upload_ex}")
                    import traceback
                    traceback.print_exc()
                    raise
        except Exception as ex:
            print(f"Erro ao processar arquivo: {ex}")
            import traceback
            traceback.print_exc()
            
            # Show error message
            if hasattr(self._page, 'show_notification'):
                self._page.show_notification(f"❌ Erro ao carregar arquivo: {str(ex)}", ft.colors.RED, duration=5)
    
    def _on_upload_complete(self, e: ft.FilePickerUploadEvent) -> None:
        """Called when file upload is complete in web mode"""
        try:
            print(f"Upload completo: {e.file_name}")
            
            if e.error:
                print(f"Erro no upload: {e.error}")
                if hasattr(self._page, 'show_notification'):
                    self._page.show_notification(f"❌ Erro no upload: {e.error}", ft.colors.RED, duration=5)
                return
            
            # Give time for file to be written
            import time
            time.sleep(0.3)
            
            if self._excel_path and os.path.exists(self._excel_path):
                print(f"Arquivo encontrado: {self._excel_path}")
                # Read the Excel file
                self._df = self._file_port.read_excel(self._excel_path)
                self._rebuild_column_lists()
                self._page.update()
                
                # Show success message
                if hasattr(self._page, 'show_notification'):
                    self._page.show_notification(f"✅ Arquivo '{e.file_name}' carregado!", ft.colors.GREEN)
                print("Arquivo carregado com sucesso após upload")
            else:
                print(f"Arquivo não encontrado: {self._excel_path}")
                if os.path.exists(self._upload_dir):
                    print(f"Arquivos em {self._upload_dir}: {os.listdir(self._upload_dir)}")
                    
                if hasattr(self._page, 'show_notification'):
                    self._page.show_notification("❌ Arquivo não foi encontrado após upload", ft.colors.RED, duration=5)
        except Exception as ex:
            print(f"Erro ao processar arquivo após upload: {ex}")
            import traceback
            traceback.print_exc()
            
            if hasattr(self._page, 'show_notification'):
                self._page.show_notification(f"❌ Erro: {str(ex)}", ft.colors.RED, duration=5)

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
            # Close the modal
            self.close()
            self._on_train(self._excel_path, columns, model)

    # -- Public API ----------------------------------------------------------

    def open(self) -> None:
        print("Abrindo modal de filtro de colunas...")
        try:
            # Build the modal content
            content = self._build_modal_content()
            
            # Create a fullscreen semi-transparent backdrop with the dialog content centered
            self._modal_container.content = ft.Stack([
                # Semi-transparent backdrop
                ft.Container(
                    bgcolor="black54",
                    expand=True,
                    on_click=lambda _: self.close(),  # Click outside to close
                ),
                # Centered dialog content
                ft.Container(
                    content=content,
                    alignment=ft.alignment.center,
                    expand=True,
                )
            ])
            self._modal_container.visible = True
            self._modal_container.expand = True
            try:
                self._page.update()
                print("Modal de filtro aberto com sucesso")
            except Exception as update_error:
                print(f"Erro ao atualizar página após abrir modal: {update_error}")
                # Tentar recuperar fechando o modal
                self.close()
                raise
        except Exception as e:
            print(f"Erro ao abrir modal: {e}")
            import traceback
            traceback.print_exc()
            # Garantir que modal está fechado em caso de erro
            self._modal_container.visible = False
            self._modal_container.content = None
            try:
                self._page.update()
            except:
                pass
    
    def close(self) -> None:
        """Close the modal"""
        self._is_modal_open = False
        self._modal_container.visible = False
        self._modal_container.expand = False
        # Clear modal content to prevent visual bugs
        self._modal_container.content = None
        self._page.update()
        print("Modal fechado e limpo")


    def _build_modal_content(self) -> ft.Container:
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

        return ft.Container(
            width=700,
            height=600,
            bgcolor=ft.colors.WHITE,
            border_radius=12,
            padding=20,
            shadow=ft.BoxShadow(
                blur_radius=30,
                spread_radius=0,
                offset=ft.Offset(0, 5),
                color="black26",
            ),
            content=ft.Column([
                ft.Row([
                    ft.Text("Filtrar Colunas", size=20, weight=ft.FontWeight.BOLD),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        on_click=lambda _: self.close(),
                        tooltip="Fechar"
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
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
                ft.Row([exclude_container, buttons, include_container], expand=True),
                ft.Text(
                    "Escolha qual IA quer utilizar:",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
                self._model_dropdown,
                ft.Divider(),
                ft.Row([
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
                ], alignment=ft.MainAxisAlignment.END)
            ], spacing=10)
        )
