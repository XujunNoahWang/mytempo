"""
Upload interface for MyTempo application.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Callable, List, Optional

from src.utils.constants import (COLORS, MAIN_WINDOW_HEIGHT, MAIN_WINDOW_WIDTH,
                                 PADDING, SUPPORTED_EXTENSIONS)


class UploadInterface:
    """File upload interface with file selection support"""
    
    def __init__(self, root: tk.Tk, on_file_selected: Callable[[List[str]], None]) -> None:
        """Initialize upload interface.
        
        Args:
            root: Main window
            on_file_selected: Callback function when files are selected
        """
        self.root = root
        self.on_file_selected = on_file_selected
        self.card_width = 340  # Card width
        self.card_height = 340  # Card height
        # Use screen center to locate geometry
        window_width = MAIN_WINDOW_WIDTH
        window_height = MAIN_WINDOW_HEIGHT
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(window_width, window_height)
        self.root.title("My Tempo")
        self.root.configure(bg=COLORS['main_bg'])
        
        # Set window icon
        from src.utils.icon_setter import set_window_icon
        set_window_icon(self.root)
        
        # Set up styles - Import StyleManager here to avoid circular import
        from src.ui.styles import StyleManager
        StyleManager.setup_styles()
        
        # Create interface
        self.create_upload_interface()
        
        # Ensure all widgets are created before centering window
        self.root.update_idletasks()
        
    def create_rounded_rectangle(self, canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, 
                               radius: int = 12, **kwargs) -> int:
        """Create rounded rectangle on canvas.
        
        Args:
            canvas: Canvas to draw on
            x1, y1, x2, y2: Rectangle coordinates
            radius: Corner radius
            **kwargs: Additional canvas options
            
        Returns:
            Canvas item ID
        """
        points = []
        for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
                     (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
                     (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
                     (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
            points.extend([x, y])
        return canvas.create_polygon(points, smooth=True, **kwargs)
        
    def draw_rounded_rect(self, event: Optional[tk.Event] = None) -> None:
        """Draw rounded rectangle background."""
        self.drop_canvas.delete("bg_rect")
        width = self.drop_canvas.winfo_width()
        height = self.drop_canvas.winfo_height()
        
        if width > 1 and height > 1:
            self.create_rounded_rectangle(
                self.drop_canvas,
                8, 8, width-8, height-8, 
                radius=12, 
                fill=COLORS['white'], 
                outline=COLORS['border'], 
                width=1,
                tags="bg_rect"
            )
            
            # Center card
            x = (width - self.card_width) // 2
            y = (height - self.card_height) // 2
            self.drop_canvas.coords(self.canvas_frame, x, y)
            self.drop_frame.configure(width=self.card_width, height=self.card_height)
            
    def create_upload_interface(self) -> None:
        """Create file upload interface."""
        main_frame = tk.Frame(self.root, bg=COLORS['main_bg'])
        main_frame.pack(expand=True, fill='both', padx=PADDING['main'], pady=PADDING['main'])
        
        drop_container = tk.Frame(main_frame, bg=COLORS['main_bg'])
        drop_container.pack(expand=True, fill='both')
        
        self.drop_canvas = tk.Canvas(drop_container, 
                                   bg=COLORS['main_bg'], 
                                   highlightthickness=0,
                                   relief='flat')
        self.drop_canvas.pack(expand=True, fill='both')
        
        self.drop_canvas.bind('<Configure>', self.draw_rounded_rect)
        
        self.drop_frame = tk.Frame(self.drop_canvas, bg=COLORS['white'], width=self.card_width, height=self.card_height)
        self.canvas_frame = self.drop_canvas.create_window(0, 0, anchor='nw', window=self.drop_frame, width=self.card_width, height=self.card_height)
        
        # Let drop_frame adapt to canvas
        self.drop_frame.pack_propagate(False)
        
        # Fill content area with pack
        drop_content_frame = tk.Frame(self.drop_frame, bg=COLORS['white'])
        drop_content_frame.pack(expand=True, fill='both')
        
        # File icon
        tk.Label(drop_content_frame,
                text="📄",
                font=('Inter', 48),
                bg=COLORS['white'],
                fg=COLORS['primary']).pack(pady=(0, 16))
        
        # Main text
        tk.Label(drop_content_frame,
                text="Select Markdown files",
                font=('Inter', 16, 'bold'),
                fg=COLORS['text_primary'],
                bg=COLORS['white']).pack(pady=(0, 8))
        
        # Sub text
        tk.Label(drop_content_frame,
                text="Click the button below to browse",
                font=('Inter', 12),
                fg=COLORS['text_secondary'],
                bg=COLORS['white']).pack(pady=(0, 24))
        
        # Button frame
        button_frame = tk.Frame(drop_content_frame, bg=COLORS['white'])
        button_frame.pack(pady=6)
        
        self.button_canvas = tk.Canvas(button_frame, 
                                     width=140, height=44,
                                     bg=COLORS['white'], 
                                     highlightthickness=0)
        self.button_canvas.pack()
        
        self.button_bg = self.create_rounded_rectangle(
            self.button_canvas,
            2, 2, 138, 42,
            radius=10,
            fill=COLORS['primary'],
            outline='',
            tags="button_bg"
        )
        
        self.button_text = self.button_canvas.create_text(
            70, 22,
            text="Browse Files",
            font=('Inter', 15, 'bold'),
            fill=COLORS['white'],
            tags="button_text"
        )
        
        # Button events
        self.button_canvas.bind('<Button-1>', lambda e: self.select_file())
        self.button_canvas.bind('<Enter>', self.on_button_enter)
        self.button_canvas.bind('<Leave>', self.on_button_leave)
        self.button_canvas.configure(cursor='hand2')
        
    def on_button_enter(self, event: Optional[tk.Event] = None) -> None:
        """Handle mouse enter button."""
        self.button_canvas.delete("button_bg")
        self.button_bg = self.create_rounded_rectangle(
            self.button_canvas,
            2, 2, 138, 42,
            radius=10,
            fill=COLORS['primary_hover'],
            outline='',
            tags="button_bg"
        )
        self.button_canvas.tag_raise("button_text")
        
    def on_button_leave(self, event: Optional[tk.Event] = None) -> None:
        """Handle mouse leave button."""
        self.button_canvas.delete("button_bg")
        self.button_bg = self.create_rounded_rectangle(
            self.button_canvas,
            2, 2, 138, 42,
            radius=10,
            fill=COLORS['primary'],
            outline='',
            tags="button_bg"
        )
        self.button_canvas.tag_raise("button_text")
        
    def select_file(self) -> None:
        """Open file dialog to select files."""
        file_paths = filedialog.askopenfilenames(
            title="Select Markdown files",
            filetypes=[
                ("Markdown files", "*.md *.markdown"),
                ("All files", "*.*")
            ]
        )
        if file_paths:
            self.process_files(list(file_paths))
    
    def process_files(self, file_paths: List[str]) -> None:
        """Process selected files.
        
        Args:
            file_paths: List of selected file paths
        """
        # Filter for supported extensions
        valid_files = []
        for file_path in file_paths:
            if any(file_path.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                valid_files.append(file_path)
            else:
                messagebox.showwarning(
                    "Unsupported file type",
                    f"File {file_path} is not a supported Markdown file."
                )
        
        if valid_files:
            self.on_file_selected(valid_files) 