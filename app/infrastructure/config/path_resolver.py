from __future__ import annotations

import os
import sys


def resolve_path(relative_path: str) -> str:
    """Resolve a relative path against the executable directory or the module directory.

    This supports both packaged (PyInstaller) and development environments.
    """
    # Try from executable location first (for packaged apps)
    exe_dir = os.path.dirname(sys.executable)
    exe_path = os.path.join(exe_dir, relative_path)

    if os.path.exists(exe_path):
        return exe_path

    # Fall back to location relative to this file
    file_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(file_dir, relative_path)

    if os.path.exists(file_path):
        return file_path

    # Ultimate fallback: relative to the app root (src/app)
    app_dir = os.path.dirname(os.path.dirname(file_dir))
    app_path = os.path.join(app_dir, relative_path)

    if os.path.exists(app_path):
        return app_path

    raise FileNotFoundError(
        f"Could not resolve path '{relative_path}' from any known base directory."
    )
