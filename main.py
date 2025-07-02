import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinterdnd2 as tkdnd
import os
import time
from typing import List, Tuple, Optional
from font_loader import load_fonts

__version__ = '0.1.1'

class LoadingWindow:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window initially
        self.root.title("Loading Fonts")
        
        # Set window size and position
        window_width = 400
        window_height = 150
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
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
        self.frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.9, relheight=0.8)
        
        # Loading text
        self.loading_label = tk.Label(
            self.frame,
            text="Loading Fonts...",
            font=('Arial', 14, 'bold'),
            bg='#ffffff',
            fg='#1d1d1f'
        )
        self.loading_label.pack(pady=(20, 10))
        
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
        self.progress_bar.pack(pady=5)
        
        # Current loading font name
        self.font_label = tk.Label(
            self.frame,
            text="Preparing...",
            font=('Arial', 10),
            bg='#ffffff',
            fg='#86868b'
        )
        self.font_label.pack(pady=5)
        
        self.start_time = time.time()
        self.root.update()
        self.root.deiconify()  # Show window
        
    def update_progress(self, current: int, total: int, font_name: str) -> None:
        """Update loading progress
        
        Args:
            current: Current progress
            total: Total items
            font_name: Current font name
        """
        progress = (current / total) * 100
        self.progress_var.set(progress)
        self.font_label.config(text=f"Loading: {font_name}")
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
        self.font_label.config(text="Loading Complete")
        self.root.update()
        time.sleep(0.2)  # Brief display of completion status

class MyTempoApp:
    def __init__(self) -> None:
        # Show loading window
        loading_window = LoadingWindow()
        
        # Pre-create main window but don't show
        self.root = tkdnd.Tk()
        self.root.withdraw()
        self.root.title("My Tempo")
        self.root.geometry("600x450")
        self.root.configure(bg='#f5f5f7')
        
        # Load fonts
        load_fonts(loading_window.update_progress)
        
        # Ensure minimum display time
        loading_window.ensure_minimum_time()
        
        # Set up main window (before showing)
        self.center_window()
        self.setup_styles()
        self.create_upload_interface()
        self.setup_drag_drop()
        
        # Close loading window and show main window
        self.root.update()
        loading_window.root.destroy()
        self.root.deiconify()
        
    def center_window(self) -> None:
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
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
            # TODO: Process valid Markdown files
            pass
            
    def run(self) -> None:
        """Run the application"""
        self.root.mainloop()

if __name__ == '__main__':
    app = MyTempoApp()
    app.run() 