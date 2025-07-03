"""
Loading window for MyTempo application.
"""

import tkinter as tk
from tkinter import ttk
import time
from typing import Optional, Callable
from ..utils.constants import COLORS, MIN_LOADING_TIME, LOADING_COMPLETE_DELAY


class LoadingWindow:
    """Loading window with progress bar"""
    
    def __init__(self, parent: Optional[tk.Tk] = None, title: str = "Loading") -> None:
        """Initialize loading window.
        
        Args:
            parent: Parent window
            title: Loading window title
        """
        self.parent = parent
        if parent:
            self.root = tk.Toplevel(parent)
        else:
            self.root = tk.Tk()
            
        self.root.withdraw()  # Always hide initially
        self.root.title(title)
        
        # Set window size and position
        window_width = 400
        window_height = 180
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate window position to center it
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set window size and position
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Set window style
        self.root.configure(bg=COLORS['white'])
        self.root.overrideredirect(True)  # Remove window decorations
        
        # Create a frame with shadow
        self.frame = tk.Frame(
            self.root,
            bg=COLORS['white'],
            highlightbackground=COLORS['border'],
            highlightthickness=1
        )
        self.frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.9, relheight=0.85)
        
        # Loading text
        self.loading_label = tk.Label(
            self.frame,
            text=title + "...",
            font=('Inter', 14, 'bold'),
            bg=COLORS['white'],
            fg=COLORS['text_primary']
        )
        self.loading_label.pack(pady=(25, 15))
        
        # Progress bar
        from .styles import StyleManager
        progress_style = StyleManager.configure_progress_bar_style()
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.frame,
            style=progress_style,
            variable=self.progress_var,
            maximum=100,
            length=300,
            mode='determinate'
        )
        self.progress_bar.pack(pady=(0, 10))
        
        # Current loading item name
        self.item_label = tk.Label(
            self.frame,
            text="Preparing...",
            font=('Inter', 10),
            bg=COLORS['white'],
            fg=COLORS['text_secondary'],
            wraplength=280
        )
        self.item_label.pack(pady=(0, 20))
        
        self.start_time = time.time()
        self.root.update()
        self.root.deiconify()  # Show window
        
    def update_progress(self, current: int, total: int, item_name: str) -> None:
        """Update loading progress.
        
        Args:
            current: Current progress
            total: Total items
            item_name: Current item name
        """
        progress = (current / total) * 100
        self.progress_var.set(progress)
        self.item_label.config(text=f"Loading: {item_name}")
        self.root.update()
        
    def ensure_minimum_time(self) -> None:
        """Ensure loading window displays for minimum time."""
        elapsed_time = time.time() - self.start_time
        min_display_time = MIN_LOADING_TIME
        
        if elapsed_time < min_display_time:
            remaining = min_display_time - elapsed_time
            time.sleep(remaining)
            
        # Show 100% completion before closing
        self.progress_var.set(100)
        self.item_label.config(text="Loading Complete")
        self.root.update()
        time.sleep(LOADING_COMPLETE_DELAY)
        
    def destroy(self) -> None:
        """Destroy loading window and return focus to parent window."""
        self.root.destroy()
        if self.parent:
            self.parent.focus_force()  # Force focus back to parent window 