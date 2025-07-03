import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkFont
import tkinterdnd2 as tkdnd
import os
import time
import re
import json
from typing import List, Tuple, Optional, Dict, Any
from font_loader import load_fonts

__version__ = '0.4.3'  # Font library simplified

class UserConfig:
    """User configuration management class"""
    def __init__(self, config_file: str = "user_settings.json") -> None:
        self.config_file = config_file
        self.default_settings = {
            "font_size": 24,
            "speed_index": 0,
            "opacity_index": 5,
            "window_width": 800,
            "window_height": 600
        }
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from config file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    # Merge default settings to ensure all necessary keys exist
                    merged_settings = self.default_settings.copy()
                    merged_settings.update(settings)
                    return merged_settings
            else:
                return self.default_settings.copy()
        except Exception as e:
            print(f"Error loading settings: {e}")
            return self.default_settings.copy()
    
    def save_settings(self) -> None:
        """Save settings to config file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get setting value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set value and save"""
        self.settings[key] = value
        self.save_settings()
    
    def update_multiple(self, updates: Dict[str, Any]) -> None:
        """Batch update settings"""
        self.settings.update(updates)
        self.save_settings()

class LoadingWindow:
    def __init__(self, parent: Optional[tk.Tk] = None, title: str = "Loading") -> None:
        self.parent = parent  # Save parent window reference
        if parent:
            self.root = tk.Toplevel(parent)
        else:
            self.root = tk.Tk()
            
        self.root.withdraw()  # Always hide initially
        self.root.title(title)
        
        # Set window size and position
        window_width = 400
        window_height = 180  # Increase height to ensure text fully displays
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate window position to center it
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set window size and position
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Set window style
        self.root.configure(bg='#ffffff')
        self.root.overrideredirect(True)  # Remove window decorations
        
        # Create a frame with shadow
        self.frame = tk.Frame(
            self.root,
            bg='#ffffff',
            highlightbackground='#e5e5e7',
            highlightthickness=1
        )
        self.frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.9, relheight=0.85)
        
        # Loading text
        self.loading_label = tk.Label(
            self.frame,
            text=title + "...",
            font=('Inter', 14, 'bold'),
            bg='#ffffff',
            fg='#1d1d1f'
        )
        self.loading_label.pack(pady=(25, 15))  # Adjust vertical spacing
        
        # Progress bar
        style = ttk.Style()
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor='#f5f5f7',
            background='#007AFF',
            thickness=6
        )
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.frame,
            style="Custom.Horizontal.TProgressbar",
            variable=self.progress_var,
            maximum=100,
            length=300,
            mode='determinate'
        )
        self.progress_bar.pack(pady=(0, 10))  # Adjust vertical spacing
        
        # Current loading item name
        self.item_label = tk.Label(
            self.frame,
            text="Preparing...",
            font=('Inter', 10),
            bg='#ffffff',
            fg='#86868b',
            wraplength=280  # Add text auto-wrap
        )
        self.item_label.pack(pady=(0, 20))  # Adjust vertical spacing
        
        self.start_time = time.time()
        self.root.update()
        self.root.deiconify()  # Show window
        
    def update_progress(self, current: int, total: int, item_name: str) -> None:
        """Update loading progress
        
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
        """Ensure loading window displays for minimum time"""
        elapsed_time = time.time() - self.start_time
        min_display_time = 1.0  # Minimum display time in seconds
        
        if elapsed_time < min_display_time:
            remaining = min_display_time - elapsed_time
            time.sleep(remaining)
            
        # Show 100% completion before closing
        self.progress_var.set(100)
        self.item_label.config(text="Loading Complete")
        self.root.update()
        time.sleep(0.2)  # Brief display of completion status
        
    def destroy(self) -> None:
        """Destroy loading window and return focus to parent window"""
        self.root.destroy()
        if self.parent:
            self.parent.focus_force()  # Force focus back to parent window

class DocumentViewer:
    """Document viewer class"""
    # Version number
    VERSION = "0.4.2"  # Fully fixed horizontal line rendering problem
    
    # Supported font sizes
    FONT_SIZES = [20, 22, 24, 28, 32, 36, 48, 60, 72]
    DEFAULT_FONT_SIZE = 24

    # Scroll related configuration
    BASE_SPEED = 0.0002  # Base speed (1x)
    SCROLL_SPEEDS = [1, 2, 3, 4, 5]  # Speed multiplier list, from 1x to 5x
    DEFAULT_SPEED_INDEX = 0  # Default use 1x speed
    SCROLL_INTERVAL = 16  # Scroll update interval (milliseconds), about 60fps for best smooth effect

    # Opacity related configuration
    OPACITY_LEVELS = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]  # From opaque to transparent
    DEFAULT_OPACITY_INDEX = 5  # Default use 50% opacity

    # Default window size
    DEFAULT_WINDOW_WIDTH = 800
    DEFAULT_WINDOW_HEIGHT = 700

    def __init__(self, parent: tk.Tk, file_path: str) -> None:
        """Initialize document viewer"""
        self.parent = parent
        self.file_path = file_path
        
        # Initialize user configuration
        self.config = UserConfig()
        
        # Load user settings from config file
        self.current_font_size = self.config.get("font_size", self.DEFAULT_FONT_SIZE)
        self.current_speed_index = self.config.get("speed_index", self.DEFAULT_SPEED_INDEX)
        self.current_opacity_index = self.config.get("opacity_index", self.DEFAULT_OPACITY_INDEX)
        
        # Ensure loaded values are within valid range
        self.current_font_size = max(min(self.current_font_size, max(self.FONT_SIZES)), min(self.FONT_SIZES))
        self.current_speed_index = max(min(self.current_speed_index, len(self.SCROLL_SPEEDS) - 1), 0)
        self.current_opacity_index = max(min(self.current_opacity_index, len(self.OPACITY_LEVELS) - 1), 0)
        
        self.is_scrolling = False  # Whether scrolling
        self.scroll_id = None  # Scroll timer ID
        
        # Hide main window
        self.parent.withdraw()

        # Create document viewer window but don't show it
        self.window = tk.Toplevel(parent)
        self.window.withdraw()  # Hide main window first
        
        # Create and display loading interface
        self.loading_window = LoadingWindow(self.parent, "Loading Document")  # Use parent as parent window
        
        # Configure main window
        self.window.title(f"My Tempo - {os.path.basename(self.file_path)}")
        
        # Load window size from config, default to 800x700
        window_width = self.config.get("window_width", self.DEFAULT_WINDOW_WIDTH)
        window_height = self.config.get("window_height", self.DEFAULT_WINDOW_HEIGHT)
        
        # Get screen dimensions
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Calculate window position to center it
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Set window size and position
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Set window background color
        self.window.configure(bg='#1a1a1a')
        
        # Set window topmost
        self.window.attributes('-topmost', True)
        
        # Set initial opacity
        self.window.attributes('-alpha', self.OPACITY_LEVELS[self.current_opacity_index])
        
        # Set window close event
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        
        # Use after method to delay loading document
        self.window.after(100, self.load_document)

    def load_document(self) -> None:
        """Load document content"""
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
            
            # Set text content
            self.text_widget.config(state=tk.NORMAL)  # Temporarily enable editing
            self.text_widget.delete('1.0', tk.END)
            
            # Analyze text and apply appropriate font
            # Process by priority: Title > Horizontal line > Quote > Bold+Italic > Bold > Italic > Highlight > Normal text
            lines = content.split('\n')
            for line in lines:
                if line.startswith('# '):
                    # Process level 1 title
                    title_text = line[2:].strip()
                    for char in title_text:
                        if '\u4e00' <= char <= '\u9fff':
                            self.text_widget.insert(tk.END, char, 'zh_h1')
                        else:
                            self.text_widget.insert(tk.END, char, 'en_h1')
                    self.text_widget.insert(tk.END, '\n')
                elif line.startswith('## '):
                    # Process level 2 title
                    title_text = line[3:].strip()
                    for char in title_text:
                        if '\u4e00' <= char <= '\u9fff':
                            self.text_widget.insert(tk.END, char, 'zh_h2')
                        else:
                            self.text_widget.insert(tk.END, char, 'en_h2')
                    self.text_widget.insert(tk.END, '\n')
                elif line.startswith('### '):
                    # Process level 3 title
                    title_text = line[4:].strip()
                    for char in title_text:
                        if '\u4e00' <= char <= '\u9fff':
                            self.text_widget.insert(tk.END, char, 'zh_h3')
                        else:
                            self.text_widget.insert(tk.END, char, 'en_h3')
                    self.text_widget.insert(tk.END, '\n')
                elif line.startswith('#### '):
                    # Process level 4 title
                    title_text = line[5:].strip()
                    for char in title_text:
                        if '\u4e00' <= char <= '\u9fff':
                            self.text_widget.insert(tk.END, char, 'zh_h4')
                        else:
                            self.text_widget.insert(tk.END, char, 'en_h4')
                    self.text_widget.insert(tk.END, '\n')
                elif line.startswith('##### '):
                    # Process level 5 title
                    title_text = line[6:].strip()
                    for char in title_text:
                        if '\u4e00' <= char <= '\u9fff':
                            self.text_widget.insert(tk.END, char, 'zh_h5')
                        else:
                            self.text_widget.insert(tk.END, char, 'en_h5')
                    self.text_widget.insert(tk.END, '\n')
                elif line.startswith('###### '):
                    # Process level 6 title
                    title_text = line[7:].strip()
                    for char in title_text:
                        if '\u4e00' <= char <= '\u9fff':
                            self.text_widget.insert(tk.END, char, 'zh_h6')
                        else:
                            self.text_widget.insert(tk.END, char, 'en_h6')
                    self.text_widget.insert(tk.END, '\n')
                elif line == '---':
                    # Process horizontal line
                    # Insert a temporary short horizontal line first, will be updated later
                    self.text_widget.insert(tk.END, '─' * 10 + '\n', 'horizontal_line')
                elif line.startswith('> '):
                    # Process quoted text
                    quote_text = line[2:].strip()  # Remove > and spaces
                    # Add vertical line, use fixed small indent
                    self.text_widget.insert(tk.END, ' ' * 5 + '│ ', 'horizontal_line')
                    
                    # Process text format inside quote
                    if quote_text.startswith('***') and quote_text.endswith('***'):
                        # Bold+Italic
                        text = quote_text[3:-3]
                        for char in text:
                            if '\u4e00' <= char <= '\u9fff':
                                self.text_widget.insert(tk.END, char, ('zh_bold_italic', 'zh_quote'))
                            else:
                                self.text_widget.insert(tk.END, char, ('en_bold_italic', 'en_quote'))
                    elif quote_text.startswith('**') and quote_text.endswith('**'):
                        # Bold
                        text = quote_text[2:-2]
                        for char in text:
                            if '\u4e00' <= char <= '\u9fff':
                                self.text_widget.insert(tk.END, char, ('zh_bold', 'zh_quote'))
                            else:
                                self.text_widget.insert(tk.END, char, ('en_bold', 'en_quote'))
                    elif (quote_text.startswith('_') and quote_text.endswith('_')) or \
                         (quote_text.startswith('*') and quote_text.endswith('*')):
                        # Italic
                        text = quote_text[1:-1]
                        for char in text:
                            if '\u4e00' <= char <= '\u9fff':
                                self.text_widget.insert(tk.END, char, ('zh_italic', 'zh_quote'))
                            else:
                                self.text_widget.insert(tk.END, char, ('en_italic', 'en_quote'))
                    elif quote_text.startswith('==') and quote_text.endswith('=='):
                        # Highlight
                        text = quote_text[2:-2]
                        for char in text:
                            if '\u4e00' <= char <= '\u9fff':
                                self.text_widget.insert(tk.END, char, ('zh_highlight', 'zh_quote'))
                            else:
                                self.text_widget.insert(tk.END, char, ('en_highlight', 'en_quote'))
                    else:
                        # Normal text
                        for char in quote_text:
                            if '\u4e00' <= char <= '\u9fff':
                                self.text_widget.insert(tk.END, char, 'zh_quote')
                            else:
                                self.text_widget.insert(tk.END, char, 'en_quote')
                    self.text_widget.insert(tk.END, '\n')  # Add newline after quote block
                else:
                    # Process text format in normal text
                    def process_text(text, base_tags=()):
                        """Process text format from inside to outside
                        
                        Args:
                            text: Text to process
                            base_tags: Base tag tuple, used for stacking effects
                        
                        Returns:
                            Processed text will be directly inserted into text_widget
                        """
                        def apply_format(text, tags):
                            """Apply format to text"""
                            for char in text:
                                char_tags = []
                                if '\u4e00' <= char <= '\u9fff':
                                    base = 'zh'
                                else:
                                    base = 'en'
                                
                                # Process tag combination
                                tag_combination = '_'.join(sorted(tags))  # Sort tags to ensure consistency
                                if tag_combination:
                                    char_tags.append(f'{base}_{tag_combination}')
                                else:
                                    char_tags.append(base)
                                
                                self.text_widget.insert(tk.END, char, tuple(char_tags))

                        # Process text format
                        def process_formats(text, current_tags):
                            """Process text format"""
                            # Try to match different formats
                            bold_match = re.search(r'\*\*(.*?)\*\*', text)
                            highlight_match = re.search(r'==(.*?)==', text)
                            italic_match = re.search(r'[*_](.*?)[*_]', text)  # Match *text* or _text_

                            if not any([bold_match, highlight_match, italic_match]):
                                # If no format mark is found, output text directly
                                apply_format(text, current_tags)
                                return

                            # Select the first found in the found format marks
                            matches = []
                            if bold_match:
                                matches.append(('bold', bold_match))
                            if highlight_match:
                                matches.append(('highlight', highlight_match))
                            if italic_match:
                                matches.append(('italic', italic_match))

                            # Sort by start position
                            matches.sort(key=lambda x: x[1].start())
                            format_type, match = matches[0]

                            # Process text before format mark
                            if match.start() > 0:
                                apply_format(text[:match.start()], current_tags)

                            # Process text with format
                            inner_text = match.group(1)
                            process_formats(inner_text, current_tags + [format_type])

                            # Process text after format mark
                            if match.end() < len(text):
                                process_formats(text[match.end():], current_tags)

                        # Start processing text
                        process_formats(text, [])

                    # Process each line
                    process_text(line)
                    if line:  # If not empty line, add newline
                        self.text_widget.insert(tk.END, '\n')
            
            self.text_widget.config(state=tk.DISABLED)  # Re-disable editing
            
            # Bind keyboard events
            self.bind_keyboard_events()
            
            # Ensure opacity setting is correct
            self.window.attributes('-alpha', self.OPACITY_LEVELS[self.current_opacity_index])
            
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
            self.text_widget.focus_set()  # Focus to text area
            
            # Wait for window to fully render before updating horizontal line length
            # Use multiple attempts to ensure window fully renders
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
        """Create text widget"""
        # Create text widget
        self.text_widget = tk.Text(
            self.window,
            font=('Noto Sans SC', self.current_font_size),  # Default use Chinese font
            bg='#1a1a1a',  # Dark background
            fg='#ffffff',  # White text
            insertbackground='#ffffff',  # White cursor
            wrap=tk.WORD,  # Word wrap
            padx=40,  # Left and right inner padding
            pady=40,  # Top and bottom inner padding
            spacing1=8,  # Paragraph spacing
            cursor='arrow'  # Use arrow cursor
        )
        self.text_widget.pack(expand=True, fill='both')
        
        # Configure basic tag
        self.text_widget.tag_configure('zh', font=('Noto Sans SC', self.current_font_size))
        self.text_widget.tag_configure('en', font=('Inter', self.current_font_size))
        
        # Configure single effect tag
        self.text_widget.tag_configure('zh_bold', font=('Noto Sans SC', self.current_font_size, 'bold'))
        self.text_widget.tag_configure('en_bold', font=('Inter', self.current_font_size, 'bold'))
        
        self.text_widget.tag_configure('zh_italic', font=('Noto Sans SC', self.current_font_size, 'italic'))
        self.text_widget.tag_configure('en_italic', font=('Inter', self.current_font_size, 'italic'))
        
        self.text_widget.tag_configure('zh_highlight', font=('Noto Sans SC', self.current_font_size), background='#404040')
        self.text_widget.tag_configure('en_highlight', font=('Inter', self.current_font_size), background='#404040')
        
        # Configure combined effect tag
        self.text_widget.tag_configure('zh_bold_highlight', font=('Noto Sans SC', self.current_font_size, 'bold'), background='#404040')
        self.text_widget.tag_configure('en_bold_highlight', font=('Inter', self.current_font_size, 'bold'), background='#404040')
        
        self.text_widget.tag_configure('zh_italic_highlight', font=('Noto Sans SC', self.current_font_size, 'italic'), background='#404040')
        self.text_widget.tag_configure('en_italic_highlight', font=('Inter', self.current_font_size, 'italic'), background='#404040')
        
        self.text_widget.tag_configure('zh_bold_italic', font=('Noto Sans SC', self.current_font_size, 'bold italic'))
        self.text_widget.tag_configure('en_bold_italic', font=('Inter', self.current_font_size, 'bold italic'))
        
        self.text_widget.tag_configure('zh_bold_italic_highlight', font=('Noto Sans SC', self.current_font_size, 'bold italic'), background='#404040')
        self.text_widget.tag_configure('en_bold_italic_highlight', font=('Inter', self.current_font_size, 'bold italic'), background='#404040')
        
        # Configure other tags
        self.text_widget.tag_configure('horizontal_line', font=('Inter', self.current_font_size), foreground='#666666')
        
        # Configure quote tag
        self.text_widget.tag_configure('zh_quote', font=('Noto Sans SC', self.current_font_size, 'bold'), 
                                     lmargin1=20, lmargin2=20)
        self.text_widget.tag_configure('en_quote', font=('Inter', self.current_font_size, 'bold'), 
                                     lmargin1=20, lmargin2=20)
        
        # Configure level title tags
        for level in range(1, 7):
            heading_size = self.get_heading_font_size(level)
            self.text_widget.tag_configure(f'zh_h{level}', font=('Noto Sans SC', heading_size, 'bold'))
            self.text_widget.tag_configure(f'en_h{level}', font=('Inter', heading_size, 'bold'))
        
        # Disable text editing
        self.text_widget.config(state=tk.DISABLED)
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure text widget scroll
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Bind window size change event
        self.window.bind('<Configure>', self.on_window_resize)

    def update_window_title(self) -> None:
        """Update window title, including file name, font size, scroll speed, and opacity information"""
        speed_multiplier = self.SCROLL_SPEEDS[self.current_speed_index]
        opacity_percentage = int(self.OPACITY_LEVELS[self.current_opacity_index] * 100)
        title = f"My Tempo - {os.path.basename(self.file_path)} - Size: {self.current_font_size}px (←→) - Speed: {speed_multiplier}x (+-) - Opacity: {opacity_percentage}% (*/)"
        self.window.title(title)

    def calculate_horizontal_line_length(self) -> int:
        """Calculate horizontal line length based on text area width"""
        try:
            # Get text area width (pixels)
            text_width = self.text_widget.winfo_width()
            
            # Subtract left and right inner padding (padx=40, so total 80 pixels)
            available_width = text_width - 80
            
            # Estimate single character width
            # Use tkinter's font.measure method to get accurate character width
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

    def get_heading_font_size(self, level: int) -> int:
        """Calculate font size based on title level"""
        multipliers = {1: 2.0, 2: 1.5, 3: 1.25, 4: 1.1, 5: 1.0, 6: 0.9}
        return int(self.current_font_size * multipliers.get(level, 1.0))

    def handle_left_key(self, event: tk.Event) -> str:
        """Handle left key event"""
        self.decrease_font_size()
        return 'break'

    def handle_right_key(self, event: tk.Event) -> str:
        """Handle right key event"""
        self.increase_font_size()
        return 'break'

    def decrease_font_size(self) -> None:
        """Decrease font size"""
        if self.current_font_size > 20:
            self.current_font_size = next(size for size in reversed(self.FONT_SIZES) if size < self.current_font_size)
            self.update_font_size()
            # Save font size setting
            self.config.set("font_size", self.current_font_size)

    def increase_font_size(self) -> None:
        """Increase font size"""
        if self.current_font_size < 72:
            self.current_font_size = next(size for size in self.FONT_SIZES if size > self.current_font_size)
            self.update_font_size()
            # Save font size setting
            self.config.set("font_size", self.current_font_size)

    def update_font_size(self) -> None:
        """Update font size"""
        if hasattr(self, 'text_widget'):
            # Save current scroll position
            current_position = self.text_widget.yview()
            
            # Update font size
            self.text_widget.configure(font=('Noto Sans SC', self.current_font_size))
            self.text_widget.tag_configure('zh', font=('Noto Sans SC', self.current_font_size))
            self.text_widget.tag_configure('en', font=('Inter', self.current_font_size))
            self.text_widget.tag_configure('zh_italic', font=('Noto Sans SC', self.current_font_size, 'italic'))
            self.text_widget.tag_configure('en_italic', font=('Inter', self.current_font_size, 'italic'))
            self.text_widget.tag_configure('zh_bold', font=('Noto Sans SC', self.current_font_size, 'bold'))
            self.text_widget.tag_configure('en_bold', font=('Inter', self.current_font_size, 'bold'))
            self.text_widget.tag_configure('zh_bold_italic', font=('Noto Sans SC', self.current_font_size, 'bold italic'))
            self.text_widget.tag_configure('en_bold_italic', font=('Inter', self.current_font_size, 'bold italic'))
            self.text_widget.tag_configure('zh_highlight', font=('Noto Sans SC', self.current_font_size), background='#404040')
            self.text_widget.tag_configure('en_highlight', font=('Inter', self.current_font_size), background='#404040')
            
            # Update quote style
            self.text_widget.tag_configure('zh_quote', font=('Noto Sans SC', self.current_font_size, 'bold'), 
                                         lmargin1=20, lmargin2=20)
            self.text_widget.tag_configure('en_quote', font=('Inter', self.current_font_size, 'bold'), 
                                         lmargin1=20, lmargin2=20)
            
            # Update level title tags
            for level in range(1, 7):
                heading_size = self.get_heading_font_size(level)
                self.text_widget.tag_configure(f'zh_h{level}', font=('Noto Sans SC', heading_size, 'bold'))
                self.text_widget.tag_configure(f'en_h{level}', font=('Inter', heading_size, 'bold'))
            
            # Restore scroll position
            self.text_widget.yview_moveto(current_position[0])
            
            # Update window title
            self.update_window_title()

    def center_window(self) -> None:
        """Center window display (only used when need to center again, like when window size changes)"""
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
        """Bind all keyboard events"""
        # Disable text widget default left and right key bindings, and rebind for font size adjustment
        self.text_widget.bind('<Left>', self.handle_left_key)
        self.text_widget.bind('<Right>', self.handle_right_key)
        
        # Window level shortcut keys
        self.window.bind('<Escape>', lambda e: self.close_window())
        self.window.bind('<Control-w>', lambda e: self.close_window())
        
        # Scroll speed adjustment
        self.window.bind('<plus>', self.increase_scroll_speed)  # + key
        self.window.bind('<minus>', self.decrease_scroll_speed)  # - key

        # Opacity adjustment
        self.window.bind('<asterisk>', self.increase_opacity)  # * key
        self.window.bind('<slash>', self.decrease_opacity)     # / key
        
        # Text widget level navigation keys
        self.text_widget.bind('<Up>', self.scroll_up)
        self.text_widget.bind('<Down>', self.start_smooth_scroll)  # Press to start scrolling
        self.text_widget.bind('<KeyRelease-Down>', self.stop_smooth_scroll)  # Release to stop scrolling
        self.text_widget.bind('<Prior>', self.page_up)  # Page Up
        self.text_widget.bind('<Next>', self.page_down)  # Page Down
        self.text_widget.bind('<Home>', self.go_to_start)  # Home
        self.text_widget.bind('<End>', self.go_to_end)  # End

    def scroll_up(self, event: tk.Event) -> str:
        """Scroll up"""
        self.text_widget.yview_scroll(-1, 'units')
        return 'break'  # Prevent default cursor movement behavior
        
    def scroll_down(self, event: tk.Event) -> str:
        """Scroll down"""
        self.text_widget.yview_scroll(1, 'units')
        return 'break'  # Prevent default cursor movement behavior
        
    def page_up(self, event: tk.Event) -> str:
        """Scroll up page"""
        self.text_widget.yview_scroll(-1, 'pages')
        return 'break'  # Prevent default cursor movement behavior
        
    def page_down(self, event: tk.Event) -> str:
        """Scroll down page"""
        self.text_widget.yview_scroll(1, 'pages')
        return 'break'  # Prevent default cursor movement behavior
        
    def go_to_start(self, event: tk.Event) -> str:
        """Jump to start"""
        self.text_widget.yview_moveto(0)
        return 'break'  # Prevent default cursor movement behavior
        
    def go_to_end(self, event: tk.Event) -> str:
        """Jump to end"""
        self.text_widget.yview_moveto(1)
        return 'break'  # Prevent default cursor movement behavior

    def start_smooth_scroll(self, event: tk.Event = None) -> str:
        """Start smooth scroll"""
        if not self.is_scrolling:
            self.is_scrolling = True
            self.smooth_scroll()
        return 'break'

    def stop_smooth_scroll(self, event: tk.Event = None) -> str:
        """Stop smooth scroll"""
        self.is_scrolling = False
        if self.scroll_id:
            self.window.after_cancel(self.scroll_id)
            self.scroll_id = None
        return 'break'

    def smooth_scroll(self) -> None:
        """Execute smooth scroll"""
        if self.is_scrolling:
            # Get current scroll position
            current_pos = self.text_widget.yview()[0]
            
            # If not at bottom, continue scrolling
            if current_pos < 1.0:
                # Use current speed multiplier to calculate actual scroll speed
                speed_multiplier = self.SCROLL_SPEEDS[self.current_speed_index]
                current_speed = self.BASE_SPEED * speed_multiplier
                self.text_widget.yview_moveto(current_pos + current_speed)
                self.scroll_id = self.window.after(self.SCROLL_INTERVAL, self.smooth_scroll)
            else:
                self.stop_smooth_scroll()

    def close_window(self) -> None:
        """Close window and show main window"""
        # Ensure stop all scrolling
        self.stop_smooth_scroll()
        
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

    def increase_scroll_speed(self, event: tk.Event = None) -> str:
        """Increase scroll speed"""
        if self.current_speed_index < len(self.SCROLL_SPEEDS) - 1:
            self.current_speed_index += 1
            self.update_window_title()
            # Save speed setting
            self.config.set("speed_index", self.current_speed_index)
        return 'break'

    def decrease_scroll_speed(self, event: tk.Event = None) -> str:
        """Decrease scroll speed"""
        if self.current_speed_index > 0:
            self.current_speed_index -= 1
            self.update_window_title()
            # Save speed setting
            self.config.set("speed_index", self.current_speed_index)
        return 'break'

    def increase_opacity(self, event: tk.Event = None) -> str:
        """Increase opacity"""
        if self.current_opacity_index > 0:
            self.current_opacity_index -= 1
            self.window.attributes('-alpha', self.OPACITY_LEVELS[self.current_opacity_index])
            self.update_window_title()
            # Save opacity setting
            self.config.set("opacity_index", self.current_opacity_index)
        return 'break'

    def decrease_opacity(self, event: tk.Event = None) -> str:
        """Decrease opacity"""
        if self.current_opacity_index < len(self.OPACITY_LEVELS) - 1:
            self.current_opacity_index += 1
            self.window.attributes('-alpha', self.OPACITY_LEVELS[self.current_opacity_index])
            self.update_window_title()
            # Save opacity setting
            self.config.set("opacity_index", self.current_opacity_index)
        return 'break'

    def on_window_resize(self, event: Optional[tk.Event] = None) -> None:
        """Handle window size change event"""
        if event and event.widget == self.window:
            # Update all horizontal lines
            self.update_horizontal_lines()

    def update_horizontal_lines(self) -> None:
        """Update length of all horizontal lines"""
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

class MyTempoApp:
    def __init__(self) -> None:
        # Create main window first but don't show it
        self.root = tkdnd.Tk()
        self.root.withdraw()
        self.root.title("My Tempo")
        
        # Set main window size
        window_width = 600
        window_height = 450
        
        # Set window size
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.configure(bg='#f5f5f7')
        
        # Show loading window
        loading_window = LoadingWindow(self.root, "Loading Fonts")
        
        # Load fonts
        load_fonts(loading_window.update_progress)
        
        # Ensure minimum display time
        loading_window.ensure_minimum_time()
        
        # Set up main window (before showing)
        self.setup_styles()
        self.create_upload_interface()
        self.setup_drag_drop()
        
        # Center window after all components are created
        self.center_window()
        
        # Close loading window and show main window
        loading_window.destroy()
        self.root.deiconify()
        self.root.focus_force()  # Ensure main window gets focus
        
    def center_window(self) -> None:
        """Center window display"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate window position to center it
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Set window position
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def get_font(self, is_chinese: bool = False, size: int = 12, weight: str = 'normal') -> Tuple[str, int, str]:
        """Get appropriate font, Noto Sans SC for Chinese, Inter for English"""
        return ('Noto Sans SC' if is_chinese else 'Inter', size, weight)
            
    def draw_rounded_rect(self, event: Optional[tk.Event] = None) -> None:
        """Draw rounded rectangle background"""
        self.drop_canvas.delete("bg_rect")
        width = self.drop_canvas.winfo_width()
        height = self.drop_canvas.winfo_height()
        
        if width > 1 and height > 1:
            self.create_rounded_rectangle(
                self.drop_canvas,
                8, 8, width-8, height-8, 
                radius=12, 
                fill='white', 
                outline='#e5e5e7', 
                width=1,
                tags="bg_rect"
            )
            
            self.drop_frame.configure(width=width-20, height=height-20)
            self.drop_canvas.coords(self.canvas_frame, 10, 10)
            
    def create_rounded_rectangle(self, canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, 
                               radius: int = 12, **kwargs) -> int:
        """Create rounded rectangle"""
        points = []
        for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
                     (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
                     (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
                     (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
            points.extend([x, y])
        return canvas.create_polygon(points, smooth=True, **kwargs)
        
    def setup_styles(self) -> None:
        """Set up Apple-style UI"""
        style = ttk.Style()
        style.configure('Apple.TButton',
                       background='#007AFF',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        
        style.map('Apple.TButton',
                 background=[('active', '#0056CC'),
                           ('pressed', '#004499')])
        
    def create_upload_interface(self) -> None:
        """Create file upload interface"""
        main_frame = tk.Frame(self.root, bg='#f5f5f7')
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        drop_container = tk.Frame(main_frame, bg='#f5f5f7')
        drop_container.pack(expand=True, fill='both')
        
        self.drop_canvas = tk.Canvas(drop_container, 
                                   bg='#f5f5f7', 
                                   highlightthickness=0,
                                   relief='flat')
        self.drop_canvas.pack(expand=True, fill='both')
        
        self.drop_canvas.bind('<Configure>', self.draw_rounded_rect)
        
        self.drop_frame = tk.Frame(self.drop_canvas, bg='white')
        self.canvas_frame = self.drop_canvas.create_window(0, 0, anchor='nw', window=self.drop_frame)
        
        drop_content_frame = tk.Frame(self.drop_frame, bg='white')
        drop_content_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(drop_content_frame,
                text="📄",
                font=self.get_font(size=48),
                bg='white',
                fg='#007AFF').pack(pady=(0, 16))
        
        tk.Label(drop_content_frame,
                text="Drop Markdown files here",
                font=self.get_font(size=16, weight='bold'),
                fg='#1d1d1f',
                bg='white').pack(pady=(0, 8))
        
        tk.Label(drop_content_frame,
                text="or click the button below to browse",
                font=self.get_font(size=12),
                fg='#86868b',
                bg='white').pack(pady=(0, 24))
        
        button_frame = tk.Frame(drop_content_frame, bg='white')
        button_frame.pack(pady=6)
        
        self.button_canvas = tk.Canvas(button_frame, 
                                     width=140, height=44,
                                     bg='white', 
                                     highlightthickness=0)
        self.button_canvas.pack()
        
        self.button_bg = self.create_rounded_rectangle(
            self.button_canvas,
            2, 2, 138, 42,
            radius=10,
            fill='#007AFF',
            outline='',
            tags="button_bg"
        )
        
        self.button_text = self.button_canvas.create_text(
            70, 22,
            text="Browse Files",
            font=self.get_font(size=15, weight='bold'),
            fill='white',
            tags="button_text"
        )
        
        self.button_canvas.bind('<Button-1>', lambda e: self.select_file())
        self.button_canvas.bind('<Enter>', self.on_button_enter)
        self.button_canvas.bind('<Leave>', self.on_button_leave)
        self.button_canvas.configure(cursor='hand2')
        
        for widget in [self.drop_canvas, self.drop_frame]:
            widget.bind('<Enter>', self.on_drag_enter)
            widget.bind('<Leave>', self.on_drag_leave)
        
    def setup_drag_drop(self) -> None:
        """Set up drag and drop functionality"""
        for widget in [self.drop_canvas, self.drop_frame]:
            widget.drop_target_register(tkdnd.DND_FILES)
            widget.dnd_bind('<<DropEnter>>', self.on_drag_enter)
            widget.dnd_bind('<<DropLeave>>', self.on_drag_leave)
            widget.dnd_bind('<<Drop>>', self.on_file_drop)
        
    def on_drag_enter(self, event: Optional[tk.Event] = None) -> None:
        """Handle mouse enter drag area"""
        self.drop_canvas.delete("bg_rect")
        width = self.drop_canvas.winfo_width()
        height = self.drop_canvas.winfo_height()
        if width > 1 and height > 1:
            self.create_rounded_rectangle(
                self.drop_canvas,
                8, 8, width-8, height-8, 
                radius=12, 
                fill='#e3f2fd', 
                outline='#007AFF', 
                width=2,
                tags="bg_rect"
            )
        
    def on_drag_leave(self, event: Optional[tk.Event] = None) -> None:
        """Handle mouse leave drag area"""
        self.draw_rounded_rect()
        
    def on_button_enter(self, event: Optional[tk.Event] = None) -> None:
        """Handle mouse enter button"""
        self.button_canvas.delete("button_bg")
        self.button_bg = self.create_rounded_rectangle(
            self.button_canvas,
            2, 2, 138, 42,
            radius=10,
            fill='#0056CC',
            outline='',
            tags="button_bg"
        )
        self.button_canvas.tag_raise("button_text")
        
    def on_button_leave(self, event: Optional[tk.Event] = None) -> None:
        """Handle mouse leave button"""
        self.button_canvas.delete("button_bg")
        self.button_bg = self.create_rounded_rectangle(
            self.button_canvas,
            2, 2, 138, 42,
            radius=10,
            fill='#007AFF',
            outline='',
            tags="button_bg"
        )
        self.button_canvas.tag_raise("button_text")
        
    def on_file_drop(self, event: tk.Event) -> None:
        """Handle file drop event"""
        file_paths = self.root.tk.splitlist(event.data)
        self.process_files(file_paths)
        
    def select_file(self) -> None:
        """Open file selection dialog"""
        file_paths = filedialog.askopenfilenames(
            title="Select Markdown Files",
            filetypes=[("Markdown files", "*.md *.markdown")]
        )
        if file_paths:
            self.process_files(file_paths)
            
    def process_files(self, file_paths: List[str]) -> None:
        """Process selected files"""
        valid_files = []
        for file_path in file_paths:
            if file_path.lower().endswith(('.md', '.markdown')):
                valid_files.append(file_path)
            else:
                messagebox.showwarning(
                    "Invalid File Format",
                    f"File {os.path.basename(file_path)} is not a Markdown file"
                )
        
        if valid_files:
            # Process valid Markdown files - only open first file
            try:
                DocumentViewer(self.root, valid_files[0])
                if len(valid_files) > 1:
                    messagebox.showinfo(
                        "Notice",
                        f"Detected {len(valid_files)} files, currently only opening first file: \n{os.path.basename(valid_files[0])}"
                    )
            except Exception as e:
                messagebox.showerror(
                    "Failed to open file",
                    f"Cannot open file {os.path.basename(valid_files[0])}:\n{str(e)}"
                )
            
    def run(self) -> None:
        """Run the application"""
        self.root.mainloop()

if __name__ == '__main__':
    app = MyTempoApp()
    app.run() 