"""
Icon setting utility for MyTempo application.
"""

import os
import tkinter as tk
from pathlib import Path


def set_window_icon(window: tk.Tk | tk.Toplevel, icon_path: str = None) -> None:
    """Set window icon.
    
    Args:
        window: Window to set icon for
        icon_path: Path to icon file (optional, will use default if not provided)
    """
    if icon_path is None:
        # Use default icon path
        current_dir = Path(__file__).parent.parent
        icon_path = current_dir / "assets" / "icons" / "mytempo.ico"
    
    # Check if icon file exists
    if os.path.exists(icon_path):
        try:
            # Set icon for Windows
            window.iconbitmap(icon_path)
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