from __future__ import annotations

import flet as ft
import os

# Get the base directory for assets
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
assets_dir = os.path.join(base_dir, "Assets", "images")

def get_image_path(filename: str) -> str:
    """Get absolute path for an image file."""
    path = os.path.join(assets_dir, filename)
    return path if os.path.exists(path) else ""

FOOTER_IMAGES: list[ft.Image] = [
    ft.Image(src=get_image_path("capes_logo-removebg-preview.png"), width=70, height=70, fit="contain"),
    ft.Image(src=get_image_path("ufpa_logo.png"), width=70, height=70, fit="contain"),
    ft.Image(src=get_image_path("ppgsp_logo.png"), width=70, height=70, fit="contain"),
    ft.Image(src=get_image_path("lab_logo.png"), width=70, height=70, fit="contain"),
    ft.Image(src=get_image_path("pcpa_logo.png"), width=70, height=70, fit="contain"),
    ft.Image(src=get_image_path("logo-siac.png"), width=70, height=70, fit="contain"),
]
