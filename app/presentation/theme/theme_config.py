from __future__ import annotations

import flet as ft
import os


def apply_theme(page: ft.Page) -> None:
    """Apply the default FlechaSQL theme to the page."""
    page.title = "FlechaSQL"
    page.theme_mode = "light"
    page.padding = 0
    
    # Try to find icon - comment out if file doesn't exist to avoid errors
    icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Assets", "images", "icon_pcpa_logo.ico")
    if os.path.exists(icon_path):
        page.window.icon = icon_path
    
    page.window.width = 1366
    page.window.height = 900
    page.window.min_width = 600
    page.window.min_height = 700
    page.window.resizable = True
    page.window.maximizable = True
    page.window.maximized = True
    page.window.center()

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
