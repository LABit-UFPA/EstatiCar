from __future__ import annotations

import flet as ft
import os


def apply_theme(page: ft.Page) -> None:
    """Apply the modern EstatiCar theme to the page."""
    page.title = "EstatiCar"
    page.theme_mode = "light"
    page.padding = 0
    
    # Modern color scheme
    page.theme = ft.Theme(
        color_scheme_seed="#6366f1",  # Indigo primary
        use_material3=True,
    )
    
    page.bgcolor = "#f8fafc"  # Soft light background
    
    # Window configuration (only relevant for desktop)
    page.window.width = 1366
    page.window.height = 900
    page.window.min_width = 600
    page.window.min_height = 700
    page.window.resizable = True
    page.window.maximizable = True
    page.window.maximized = True

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
