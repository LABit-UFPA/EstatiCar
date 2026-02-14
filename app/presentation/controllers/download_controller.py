from __future__ import annotations

import flet as ft

from domain.use_cases.export_result import ExportResultUseCase
from presentation.state.app_state import AppState


class DownloadController:
    """Handles exporting the last query result to an Excel file."""

    def __init__(
        self,
        page: ft.Page,
        use_case: ExportResultUseCase,
        state: AppState,
    ) -> None:
        self._page = page
        self._use_case = use_case
        self._state = state

    def handle(self, e=None) -> None:
        print("Botão 'Salvar Tabela' clicado")
        if self._state.last_result is not None:
            print(f"Resultado encontrado, salvando dados...")
            
            import os
            from datetime import datetime
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resultado_{timestamp}.xlsx"
            
            # Save to uploads directory (temporary storage on server)
            upload_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                "uploads"
            )
            
            # Ensure directory exists
            os.makedirs(upload_dir, exist_ok=True)
            
            # Use case adds .xlsx, so remove it from the path
            filepath = os.path.join(upload_dir, f"resultado_{timestamp}")
            
            print(f"Salvando em: {filepath} (use case adicionará .xlsx)")
            # Don't open folder in web mode (open_folder=False)
            msg = self._use_case.execute(self._state.last_result, filepath, open_folder=False)
            print(f"Arquivo salvo: {msg}")
            print(f"Arquivo final: {filepath}.xlsx")
            
            # Use Flask download server URL (port 8081) with proper download headers
            download_url = f"http://127.0.0.1:8081/download/{filename}"
            
            # Create download button that uses the Flask endpoint
            def trigger_download(e):
                # Launch URL - Flask server will force download without opening new window
                print(f"Baixando arquivo via Flask: {download_url}")
                self._page.launch_url(download_url)
                
                # Show success notification
                if hasattr(self._page, 'show_notification'):
                    self._page.show_notification(
                        f"✅ Download iniciado: {filename}", 
                        ft.colors.GREEN, 
                        duration=3
                    )
                
                # Close modal after short delay
                import threading
                def close_later():
                    import time
                    time.sleep(0.5)
                    self._close_download_modal()
                
                threading.Thread(target=close_later, daemon=True).start()
            
            download_button = ft.ElevatedButton(
                "📥 Baixar",
                on_click=trigger_download,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.GREEN_400,
                    color=ft.colors.WHITE,
                ),
                height=40,
                width=200,
            )
            
            # Create modal container
            modal_content = ft.Container(
                content=ft.Column([
                    ft.Text("✅ Arquivo pronto!", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN),
                    download_button,
                    ft.TextButton(
                        "Fechar",
                        on_click=lambda _: self._close_download_modal(),
                    )
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8),
                padding=15,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                width=300,
                height=150,
            )
            
            # Create backdrop
            backdrop = ft.Container(
                bgcolor=ft.colors.with_opacity(0.5, ft.colors.BLACK),
                expand=True,
            )
            
            # Create modal with backdrop
            self._download_modal = ft.Container(
                content=ft.Stack([
                    backdrop,
                    ft.Container(
                        content=modal_content,
                        alignment=ft.alignment.center,
                    )
                ]),
                visible=True,
                expand=True,
            )
            
            # Add to overlay
            self._page.overlay.append(self._download_modal)
            self._page.update()
            
            print(f"Modal de download exibido. Usando Flask download server: {download_url}")
            
        else:
            print("Nenhum resultado para salvar")
            if hasattr(self._page, 'show_notification'):
                self._page.show_notification("❌ Nenhum resultado encontrado para salvar", ft.colors.RED, duration=5)
            self._page.update()
    
    def _close_download_modal(self) -> None:
        """Close the download modal"""
        if hasattr(self, '_download_modal') and self._download_modal in self._page.overlay:
            self._page.overlay.remove(self._download_modal)
            self._page.update()
