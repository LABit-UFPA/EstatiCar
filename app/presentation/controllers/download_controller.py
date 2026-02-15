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
        print("[PROCESSING] Save table button clicked")
        if self._state.last_result is not None:
            print(f"[PROCESSING] Result found, saving data...")
            
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
            
            print(f"[PROCESSING] Saving to: {filepath} (use case will add .xlsx)")
            # Don't open folder in web mode (open_folder=False)
            msg = self._use_case.execute(self._state.last_result, filepath, open_folder=False)
            print(f"[SUCCESS] File saved: {msg}")
            print(f"[PROCESSING] Final file: {filepath}.xlsx")
            
            # Build download URL - use relative URL based on current page host
            # Extract hostname from page URL or use localhost for desktop mode
            page_url = getattr(self._page, 'url', 'http://localhost:8080')
            if '://' in page_url:
                protocol_host = page_url.split('://', 1)[1].split('/', 1)[0]
                # Replace port with 8081 (Flask server port)
                if ':' in protocol_host:
                    host = protocol_host.split(':')[0]
                else:
                    host = protocol_host
            else:
                host = 'localhost'
            
            download_url = f"http://{host}:8081/download/{filename}"
            print(f"[PROCESSING] Download URL: {download_url}")
            
            # Create download button that triggers download without opening new tab
            def trigger_download(e):
                print(f"[PROCESSING] Downloading file via Flask: {download_url}")
                
                # Use HTML link with download attribute - works better in web mode
                # Create a hidden link, click it programmatically, then remove it
                js_code = f"""
                (function() {{
                    var link = document.createElement('a');
                    link.href = '{download_url}';
                    link.download = '{filename}';
                    link.style.display = 'none';
                    document.body.appendChild(link);
                    link.click();
                    setTimeout(function() {{
                        document.body.removeChild(link);
                    }}, 100);
                }})();
                """
                
                try:
                    # Try using page.js to execute JavaScript
                    if hasattr(self._page, 'js'):
                        self._page.js(js_code)
                        print("[SUCCESS] Download via JavaScript executed")
                    else:
                        # Fallback: use window.open with _self target (replaces current page temporarily)
                        print("[PROCESSING] JavaScript not available, using launch_url")
                        self._page.launch_url(download_url)
                except Exception as js_err:
                    print(f"[ERROR] JavaScript execution failed: {js_err}")
                    # Fallback: use launch_url
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
                    time.sleep(1.0)
                    self._close_download_modal()
                
                threading.Thread(target=close_later, daemon=True).start()
            
            download_button = ft.ElevatedButton(
                "📥 Baixar Arquivo",
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
                    ft.Text("✅ Arquivo pronto!", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN),
                    ft.Text(filename, size=12, color=ft.colors.GREY_700),
                    ft.Divider(),
                    download_button,
                    ft.TextButton(
                        "Fechar",
                        on_click=lambda _: self._close_download_modal(),
                    )
                ], 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10),
                padding=20,
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                width=320,
                height=200,
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
            
            print(f"[SUCCESS] Download modal displayed - URL: {download_url}")
            
        else:
            print("[ERROR] No result to save")
            if hasattr(self._page, 'show_notification'):
                self._page.show_notification("❌ Nenhum resultado encontrado para salvar", ft.colors.RED, duration=5)
            self._page.update()
    
    def _close_download_modal(self) -> None:
        """Close the download modal"""
        if hasattr(self, '_download_modal') and self._download_modal in self._page.overlay:
            self._page.overlay.remove(self._download_modal)
            self._page.update()
