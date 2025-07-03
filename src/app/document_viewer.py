"""
Document viewer for MyTempo application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import os
from typing import Optional
from src.core.config import UserConfig
from src.core.text_processor import TextProcessor
from src.core.scroll_manager import ScrollManager
from src.ui.loading_window import LoadingWindow
from src.ui.styles import StyleManager
from src.utils.constants import (
    FONT_SIZES, DEFAULT_FONT_SIZE, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT,
    OPACITY_LEVELS, DEFAULT_OPACITY_INDEX, COLORS, PADDING
)


class DocumentViewer:
    """Document viewer class for displaying Markdown files"""
    
    def __init__(self, parent: tk.Tk, file_path: str) -> None:
        """Initialize document viewer.
        
        Args:
            parent: Parent window
            file_path: Path to Markdown file
        """
        self.parent = parent
        self.file_path = file_path
        
        # Initialize user configuration
        self.config = UserConfig()
        
        # Load user settings from config file
        self.current_font_size = self.config.get("font_size", DEFAULT_FONT_SIZE)
        self.current_opacity_index = self.config.get("opacity_index", DEFAULT_OPACITY_INDEX)
        
        # Ensure loaded values are within valid range
        self.current_font_size = max(min(self.current_font_size, max(FONT_SIZES)), min(FONT_SIZES))
        self.current_opacity_index = max(min(self.current_opacity_index, len(OPACITY_LEVELS) - 1), 0)
        
        # Hide main window
        self.parent.withdraw()

        # Create document viewer window but don't show it
        self.window = tk.Toplevel(parent)
        self.window.withdraw()
        
        # Create and display loading interface
        self.loading_window = LoadingWindow(self.parent, "Loading Document")
        
        # Configure main window
        self.window.title(f"My Tempo - {os.path.basename(self.file_path)}")
        
        # Load window size from config
        window_width = self.config.get("window_width", DEFAULT_WINDOW_WIDTH)
        window_height = self.config.get("window_height", DEFAULT_WINDOW_HEIGHT)
        
        # Get screen dimensions
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Calculate window position to center it
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set window size and position
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Set window properties
        self.window.configure(bg=COLORS['background'])
        self.window.attributes('-topmost', True)
        self.window.attributes('-alpha', OPACITY_LEVELS[self.current_opacity_index])
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        
        # Use after method to delay loading document
        self.window.after(100, self.load_document)

    def load_document(self) -> None:
        """Load document content."""
        try:
            # Update loading status
            self.loading_window.update_progress(1, 4, "Creating text widget...")
            
            # Create text widget
            self.create_text_widget()
            
            # Update loading status
            self.loading_window.update_progress(2, 4, "Loading content...")
            
            # Load file content
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Update loading status
            self.loading_window.update_progress(3, 4, "Rendering content...")
            
            # Parse and render content
            self.render_content(content)
            
            # Update loading status
            self.loading_window.update_progress(4, 4, "Complete")
            
            # Ensure minimum display time
            self.loading_window.ensure_minimum_time()
            
            # Show main window
            self.window.deiconify()
            
            # Destroy loading window
            self.loading_window.destroy()
            
            # Update window title
            self.update_window_title()
            
            # Set window to front and focus to text area
            self.window.lift()
            self.window.focus_force()
            self.text_widget.focus_set()
            
            # Wait for window to fully render before updating horizontal line length
            self.window.after(100, self.update_horizontal_lines)
            self.window.after(300, self.update_horizontal_lines)
            self.window.after(500, self.update_horizontal_lines)
            
        except Exception as e:
            # If error occurs, ensure closing loading window
            if hasattr(self, 'loading_window'):
                self.loading_window.destroy()
            messagebox.showerror("Failed to open file", f"Cannot open file {os.path.basename(self.file_path)}:\n{str(e)}")
            self.close_window()

    def create_text_widget(self) -> None:
        """Create text widget with scrollbar."""
        # Create text widget
        self.text_widget = tk.Text(
            self.window,
            font=('Noto Sans SC', self.current_font_size),
            bg=COLORS['background'],
            fg=COLORS['text'],
            insertbackground=COLORS['text'],
            wrap=tk.WORD,
            padx=PADDING['text'],
            pady=PADDING['text'],
            spacing1=8,
            cursor='arrow'
        )
        self.text_widget.pack(expand=True, fill='both')
        
        # Configure text tags
        StyleManager.configure_text_tags(self.text_widget, self.current_font_size)
        
        # Disable text editing
        self.text_widget.config(state=tk.DISABLED)
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure text widget scroll
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Bind window size change event
        self.window.bind('<Configure>', self.on_window_resize)
        
        # Initialize scroll manager
        self.scroll_manager = ScrollManager(self.text_widget, self.config)
        self.scroll_manager.bind_scroll_events(self.window)
        
        # Bind keyboard events
        self.bind_keyboard_events()

    def render_content(self, content: str) -> None:
        """Render Markdown content in text widget.
        
        Args:
            content: Raw Markdown content
        """
        # Parse content
        parsed_content = TextProcessor.parse_markdown(content)
        
        # Temporarily enable editing
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete('1.0', tk.END)
        
        # Insert parsed content
        for char, tag in parsed_content:
            if tag:
                if isinstance(tag, tuple):
                    self.text_widget.insert(tk.END, char, tag)
                else:
                    self.text_widget.insert(tk.END, char, tag)
            else:
                self.text_widget.insert(tk.END, char)
        
        # Re-disable editing
        self.text_widget.config(state=tk.DISABLED)

    def update_window_title(self) -> None:
        """Update window title with current settings."""
        speed_multiplier = self.scroll_manager.get_current_speed_multiplier()
        opacity_percentage = int(OPACITY_LEVELS[self.current_opacity_index] * 100)
        title = f"My Tempo - {os.path.basename(self.file_path)} - Size: {self.current_font_size}px (←→) - Speed: {speed_multiplier}x (+-) - Opacity: {opacity_percentage}% (*/)"
        self.window.title(title)

    def calculate_horizontal_line_length(self) -> int:
        """Calculate horizontal line length based on text area width.
        
        Returns:
            Number of characters for horizontal line
        """
        try:
            # Get text area width (pixels)
            text_width = self.text_widget.winfo_width()
            
            # Subtract left and right inner padding
            available_width = text_width - (PADDING['text'] * 2)
            
            # Estimate single character width
            font = tkFont.Font(family='Inter', size=self.current_font_size)
            char_width = font.measure('─')
            
            # Calculate number of characters that can fit
            if char_width > 0:
                line_length = max(1, int(available_width / char_width))
            else:
                line_length = 60  # Default value
                
            return line_length
        except:
            # If calculation fails, return default value
            return 60

    def handle_left_key(self, event: tk.Event) -> str:
        """Handle left key event."""
        self.decrease_font_size()
        return 'break'

    def handle_right_key(self, event: tk.Event) -> str:
        """Handle right key event."""
        self.increase_font_size()
        return 'break'

    def decrease_font_size(self) -> None:
        """Decrease font size."""
        if self.current_font_size > 20:
            self.current_font_size = next(size for size in reversed(FONT_SIZES) if size < self.current_font_size)
            self.update_font_size()
            self.config.set("font_size", self.current_font_size)

    def increase_font_size(self) -> None:
        """Increase font size."""
        if self.current_font_size < 72:
            self.current_font_size = next(size for size in FONT_SIZES if size > self.current_font_size)
            self.update_font_size()
            self.config.set("font_size", self.current_font_size)

    def update_font_size(self) -> None:
        """Update font size in text widget."""
        if hasattr(self, 'text_widget'):
            # Save current scroll position
            current_position = self.text_widget.yview()
            
            # Update font size
            self.text_widget.configure(font=('Noto Sans SC', self.current_font_size))
            
            # Reconfigure text tags
            StyleManager.configure_text_tags(self.text_widget, self.current_font_size)
            
            # Restore scroll position
            self.text_widget.yview_moveto(current_position[0])
            
            # Update window title
            self.update_window_title()

    def center_window(self) -> None:
        """Center window display."""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        
        # Get screen dimensions
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Calculate window position to center it
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set window position
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def bind_keyboard_events(self) -> None:
        """Bind keyboard events."""
        # Disable text widget default left and right key bindings, and rebind for font size adjustment
        self.text_widget.bind('<Left>', self.handle_left_key)
        self.text_widget.bind('<Right>', self.handle_right_key)
        
        # Window level shortcut keys
        self.window.bind('<Escape>', lambda e: self.close_window())
        self.window.bind('<Control-w>', lambda e: self.close_window())
        
        # Opacity adjustment
        self.window.bind('<asterisk>', self.increase_opacity)
        self.window.bind('<slash>', self.decrease_opacity)

    def increase_opacity(self, event: Optional[tk.Event] = None) -> str:
        """Increase opacity."""
        if self.current_opacity_index > 0:
            self.current_opacity_index -= 1
            self.window.attributes('-alpha', OPACITY_LEVELS[self.current_opacity_index])
            self.update_window_title()
            self.config.set("opacity_index", self.current_opacity_index)
        return 'break'

    def decrease_opacity(self, event: Optional[tk.Event] = None) -> str:
        """Decrease opacity."""
        if self.current_opacity_index < len(OPACITY_LEVELS) - 1:
            self.current_opacity_index += 1
            self.window.attributes('-alpha', OPACITY_LEVELS[self.current_opacity_index])
            self.update_window_title()
            self.config.set("opacity_index", self.current_opacity_index)
        return 'break'

    def on_window_resize(self, event: Optional[tk.Event] = None) -> None:
        """Handle window size change event."""
        if event and event.widget == self.window:
            self.update_horizontal_lines()

    def update_horizontal_lines(self) -> None:
        """Update length of all horizontal lines."""
        try:
            # Get all ranges with horizontal_line tag
            ranges = self.text_widget.tag_ranges('horizontal_line')
            if not ranges:
                return
                
            # Calculate new horizontal line length
            line_length = self.calculate_horizontal_line_length()
            
            # Temporarily enable editing
            self.text_widget.config(state=tk.NORMAL)
            
            # Process two indices at a time (start and end)
            for i in range(0, len(ranges), 2):
                start = ranges[i]
                end = ranges[i + 1]
                
                # Get content of current line
                current_line = self.text_widget.get(start, end).strip()
                
                # Process only horizontal lines (lines composed of ─ characters)
                if all(c == '─' for c in current_line):
                    # Replace with new length horizontal line
                    self.text_widget.delete(start, end)
                    self.text_widget.insert(start, '─' * line_length, 'horizontal_line')
            
            # Re-disable editing
            self.text_widget.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Error updating horizontal lines: {e}")

    def close_window(self) -> None:
        """Close window and show main window."""
        # Ensure stop all scrolling
        if hasattr(self, 'scroll_manager'):
            self.scroll_manager.stop_smooth_scroll()
        
        # Save window size
        try:
            # Get current window size
            geometry = self.window.geometry()
            # Parse geometry string (e.g., "900x700+100+100")
            size_part = geometry.split('+')[0]  # Get "900x700" part
            width, height = map(int, size_part.split('x'))
            
            # Save window size setting
            self.config.update_multiple({
                "window_width": width,
                "window_height": height
            })
        except Exception as e:
            print(f"Error saving window size: {e}")
        
        self.window.destroy()
        # Re-show main window
        self.parent.deiconify() 