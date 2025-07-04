"""
Icon setting utility for MyTempo application.
"""

import os
import sys
import tkinter as tk
from pathlib import Path


def set_window_icon(window: tk.Tk | tk.Toplevel, icon_path: str = None) -> None:
    """Set window icon.
    
    Args:
        window: Window to set icon for
        icon_path: Path to icon file (optional, will use default if not provided)
    """
    if icon_path is None:
        # Try multiple possible paths for the icon
        possible_paths = []
        
        # Development path
        current_dir = Path(__file__).parent.parent
        possible_paths.append(current_dir / "assets" / "icons" / "mytempo.ico")
        
        # PyInstaller bundled path
        if hasattr(sys, '_MEIPASS'):
            # Running in PyInstaller bundle
            bundle_dir = Path(sys._MEIPASS)
            possible_paths.append(bundle_dir / "src" / "assets" / "icons" / "mytempo.ico")
        
        # Current working directory path
        possible_paths.append(Path.cwd() / "src" / "assets" / "icons" / "mytempo.ico")
        
        # Find the first existing path
        icon_path = None
        for path in possible_paths:
            if os.path.exists(path):
                icon_path = path
                break
    
    # Check if icon file exists
    if icon_path and os.path.exists(icon_path):
        try:
            # Set icon for Windows
            window.iconbitmap(str(icon_path))
        except Exception as e:
            # Fallback: try to set icon using photoimage (for other platforms)
            try:
                from PIL import Image, ImageTk
                image = Image.open(icon_path)
                photo = ImageTk.PhotoImage(image)
                window.iconphoto(True, photo)
            except ImportError:
                # PIL not available, skip icon setting
                pass
            except Exception:
                # Any other error, skip icon setting
                pass 