"""
FlechaSQL — Composition Root
============================
This is the only place where concrete implementations are instantiated and
wired together (Dependency Injection).  Every other module depends only on
abstractions (ports) or on its own layer.

Layers (inner → outer):
    domain  →  infrastructure  →  presentation
"""

import flet as ft
import os

# -- Infrastructure (concrete implementations) --------------------------------
from infrastructure.adapters.ollama_adapter import OllamaAdapter
from infrastructure.adapters.sqlite_adapter import SQLiteAdapter
from infrastructure.adapters.file_adapter import FileAdapter
from infrastructure.config.config_adapter import JsonConfigAdapter

# -- Domain (use cases) -------------------------------------------------------
from domain.use_cases.ask_question import AskQuestionUseCase
from domain.use_cases.train_model import TrainModelUseCase
from domain.use_cases.export_result import ExportResultUseCase

# -- Presentation --------------------------------------------------------------
from presentation.theme.theme_config import apply_theme
from presentation.state.app_state import AppState
from presentation.components.progress_dialog import build_progress_dialog
from presentation.components.error_dialog import ErrorDialog
from presentation.views.card_content_view import CardContentView
from presentation.views.query_content_view import QueryContentView
from presentation.views.tabs_view import TabsView
from presentation.views.input_field_view import InputFieldView
from presentation.views.footer_view import build_footer
from presentation.views.train_button_view import build_train_button
from presentation.views.download_button_view import build_download_button
from presentation.views.column_filter_view import ColumnFilterView
from presentation.controllers.question_controller import QuestionController
from presentation.controllers.training_controller import TrainingController
from presentation.controllers.download_controller import DownloadController


def main(page: ft.Page) -> None:
    try:
        # ── Theme ────────────────────────────────────────────────────────────────
        apply_theme(page)

        # ── State ────────────────────────────────────────────────────────────────
        state = AppState()

        # ── Infrastructure adapters ──────────────────────────────────────────────
        config_adapter = JsonConfigAdapter()
        
        # Get service URLs from environment variables (defaults to localhost for dev)
        qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        ai_adapter = OllamaAdapter(
            model=state.choice, 
            qdrant_url=qdrant_url,
            ollama_host=ollama_host
        )
        
        db_adapter = SQLiteAdapter()
        file_adapter = FileAdapter()

        # ── Use cases ────────────────────────────────────────────────────────
        ask_question_uc = AskQuestionUseCase(ai_model=ai_adapter, config=config_adapter)
        train_model_uc = TrainModelUseCase(
            ai_model=ai_adapter, database=db_adapter, config=config_adapter
        )
        export_result_uc = ExportResultUseCase(file_service=file_adapter)

        # ── Presentation components ──────────────────────────────────────────
        progress_dialog = build_progress_dialog()
        error_dialog = ErrorDialog(page)
        
        # Add dialogs to overlay so they can be displayed
        page.overlay.append(progress_dialog)
        page.overlay.append(error_dialog._dialog)
        page.update()  # Force update after adding overlays

        card_view = CardContentView(initial_text="O Resultado será mostrado aqui...")
        card_content = card_view.build()

        query_view = QueryContentView()
        query_content = query_view.build()

        # ── Controllers ──────────────────────────────────────────────────────
        question_ctrl = QuestionController(
            page=page,
            use_case=ask_question_uc,
            state=state,
            progress_dialog=progress_dialog,
            error_dialog=error_dialog,
            card_content=card_content,
            query_content=query_content,
        )
        training_ctrl = TrainingController(
            page=page,
            use_case=train_model_uc,
            ai_adapter=ai_adapter,
            state=state,
            progress_dialog=progress_dialog,
        )
        download_ctrl = DownloadController(
            page=page, use_case=export_result_uc, state=state
        )

        # ── Views ────────────────────────────────────────────────────────────
        def on_question(e):
            question_ctrl.handle(e, input_field_view.control)

        input_field_view = InputFieldView(on_submit=on_question, page=page)
        
        # Create buttons (will be referenced later for disabling)
        search_button = ft.IconButton(
            icon=ft.Icons.SEARCH,
            on_click=on_question,
        )

        filter_view = ColumnFilterView(
            page=page,
            state=state,
            on_train=training_ctrl.handle,
            file_port=file_adapter,
        )

        tabs = TabsView(page).build(card_content=card_content, query_content=query_content)
        train_button = build_train_button(on_click=filter_view.open)
        download_button = build_download_button(on_click=lambda e: download_ctrl.handle(e))
        footer = build_footer()
        
        # ── UI Control Manager ───────────────────────────────────────────────
        def set_ui_busy(busy: bool):
            """Enable/disable UI controls during processing"""
            input_field_view.control.disabled = busy
            search_button.disabled = busy
            train_button.disabled = busy
            download_button.disabled = busy
            page.update()
        
        # Store in page for access from controllers
        page.set_ui_busy = set_ui_busy

        # ── Notification container (web-compatible) ──────────────────────────
        notification_container = ft.Container(
            height=0,
            animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
            content=None
        )
        
        def show_notification(message: str, bgcolor: str = None, duration: int = 3):
            """Show inline notification that works in web mode"""
            if bgcolor is None:
                bgcolor = ft.colors.BLUE
            
            notification_container.content = ft.Container(
                content=ft.Text(message, color=ft.colors.WHITE, size=14, weight=ft.FontWeight.BOLD),
                bgcolor=bgcolor,
                padding=10,
                border_radius=8,
            )
            notification_container.height = 50
            page.update()
            
            # Auto-hide after duration (unless it's a long-running operation indicator)
            if duration < 100:  # Only auto-hide short notifications
                import threading
                def hide():
                    import time
                    time.sleep(duration)
                    notification_container.height = 0
                    notification_container.content = None
                    page.update()
                
                threading.Thread(target=hide, daemon=True).start()
        
        def hide_notification():
            """Manually hide notification"""
            notification_container.height = 0
            notification_container.content = None
            page.update()
        
        # Store in page for access from controllers
        page.show_notification = show_notification
        page.hide_notification = hide_notification

        # ── Page layout ──────────────────────────────────────────────────────
        page.add(
            ft.Container(
                height=page.window.height,
                width=page.window.width,
                padding=ft.padding.all(20),
                alignment=ft.alignment.center,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        notification_container,  # Add notification container at top
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                input_field_view.control,
                                search_button,
                            ],
                        ),
                        ft.SelectionArea(tabs),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[train_button, download_button],
                        ),
                        footer,
                    ],
                ),
            )
        )
        
        # ── Update page ──────────────────────────────────────────────────────
        page.update()

    except Exception as e:
        print(f"Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        # Show error in the page
        page.clean()
        page.add(
            ft.Column([
                ft.Text(f"Erro ao inicializar aplicação:", size=20, color="red"),
                ft.Text(f"{str(e)}", size=14),
            ])
        )
        page.update()


import os
from infrastructure.adapters.download_server import DownloadServer

upload_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(upload_directory, exist_ok=True)

# Start download server (Flask) on port 8081
download_server = DownloadServer(upload_directory, port=8081)
download_server.start()

# Set secret key for uploads via environment variable
os.environ["FLET_SECRET_KEY"] = "flechasql-secret-key-2026"

# Use WEB_BROWSER mode with custom modal overlays (no native dialogs)
ft.app(
    target=main, 
    view=ft.AppView.WEB_BROWSER,
    assets_dir="Assets",
    upload_dir=upload_directory,
    port=8080
)
