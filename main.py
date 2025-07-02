import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinterdnd2 as tkdnd
import os
import time
from typing import List, Tuple, Optional
from font_loader import load_fonts

__version__ = '0.1.6'

class LoadingWindow:
    def __init__(self, parent: Optional[tk.Tk] = None, title: str = "Loading") -> None:
        if parent:
            self.root = tk.Toplevel(parent)
        else:
            self.root = tk.Tk()
            
        self.root.withdraw()  # Always hide initially
        self.root.title(title)
        
        # Set window size and position
        window_width = 400
        window_height = 180  # 增加高度以确保文本完全显示
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
        self.frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.9, relheight=0.85)  # 增加frame高度比例
        
        # Loading text
        self.loading_label = tk.Label(
            self.frame,
            text=title + "...",
            font=('Inter', 14, 'bold'),
            bg='#ffffff',
            fg='#1d1d1f'
        )
        self.loading_label.pack(pady=(25, 15))  # 调整上下间距
        
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
        self.progress_bar.pack(pady=(0, 10))  # 调整上下间距
        
        # Current loading item name
        self.item_label = tk.Label(
            self.frame,
            text="Preparing...",
            font=('Inter', 10),
            bg='#ffffff',
            fg='#86868b',
            wraplength=280  # 添加文本自动换行
        )
        self.item_label.pack(pady=(0, 20))  # 调整上下间距
        
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
        """Destroy the loading window"""
        self.root.destroy()

class DocumentViewer:
    # 定义字体大小列表
    FONT_SIZES = [10, 11, 12, 14, 16, 18, 20, 22, 24, 28, 32, 36, 48, 60, 72]
    DEFAULT_FONT_SIZE = 24

    def __init__(self, parent: tk.Tk, file_path: str) -> None:
        self.parent = parent
        self.file_path = file_path
        self.current_font_size = self.DEFAULT_FONT_SIZE
        
        # 隐藏主窗口
        self.parent.withdraw()
        
        # 创建文档查看窗口
        self.window = tk.Toplevel(parent)
        self.update_window_title()  # 使用新方法更新标题
        self.window.geometry("900x700")
        self.window.configure(bg='#1a1a1a')
        
        # 设置窗口关闭事件
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        
        # 居中显示窗口
        self.center_window()
        
        # 创建并显示加载界面
        self.loading_window = LoadingWindow(self.window, "Loading Document")
        self.window.after(100, self.load_document)
        
        # 绑定键盘事件
        self.window.bind('<Left>', self.decrease_font_size)
        self.window.bind('<Right>', self.increase_font_size)

    def update_window_title(self) -> None:
        """更新窗口标题，包含文件名和字体大小信息"""
        title = f"My Tempo - {os.path.basename(self.file_path)} - Size: {self.current_font_size}px (← →)"
        self.window.title(title)

    def increase_font_size(self, event: Optional[tk.Event] = None) -> None:
        """增加字体大小"""
        current_index = self.FONT_SIZES.index(self.current_font_size)
        if current_index < len(self.FONT_SIZES) - 1:
            self.current_font_size = self.FONT_SIZES[current_index + 1]
            self.update_font_size()

    def decrease_font_size(self, event: Optional[tk.Event] = None) -> None:
        """减小字体大小"""
        current_index = self.FONT_SIZES.index(self.current_font_size)
        if current_index > 0:
            self.current_font_size = self.FONT_SIZES[current_index - 1]
            self.update_font_size()

    def update_font_size(self) -> None:
        """更新字体大小"""
        if hasattr(self, 'text_widget'):
            # 保存当前滚动位置
            current_position = self.text_widget.yview()
            
            # 更新字体配置
            self.text_widget.tag_configure('content', font=('Noto Sans SC', self.current_font_size))
            
            # 如果还没有应用tag，则应用tag
            if not self.text_widget.tag_ranges('content'):
                self.text_widget.tag_add('content', '1.0', 'end')
            
            # 恢复滚动位置
            self.text_widget.yview_moveto(current_position[0])
            
            # 更新标题
            self.update_window_title()

    def center_window(self) -> None:
        """将窗口居中显示"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def load_document(self) -> None:
        """加载文档内容"""
        try:
            # 更新加载状态
            self.loading_window.item_label.config(text=f"Reading: {os.path.basename(self.file_path)}")
            self.loading_window.progress_var.set(30)
            self.loading_window.root.update()
            
            # 读取文件内容
            content = self.read_file_content()
            
            # 更新加载状态
            self.loading_window.item_label.config(text="Preparing display")
            self.loading_window.progress_var.set(60)
            self.loading_window.root.update()
            
            # 创建界面
            self.create_interface()
            
            # 更新加载状态
            self.loading_window.item_label.config(text="Rendering content")
            self.loading_window.progress_var.set(90)
            self.loading_window.root.update()
            
            # 显示内容
            self.display_content(content)
            
            # 完成加载
            self.loading_window.progress_var.set(100)
            self.loading_window.item_label.config(text="Complete")
            self.loading_window.root.update()
            time.sleep(0.2)
            
            # 销毁加载窗口
            self.loading_window.destroy()
            
        except Exception as e:
            self.loading_window.destroy()
            self.show_error(str(e))
        
    def read_file_content(self) -> str:
        """读取文件内容"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # 尝试其他编码
            try:
                with open(self.file_path, 'r', encoding='gbk') as file:
                    return file.read()
            except Exception as e:
                raise Exception(f"无法读取文件: {str(e)}")
        except Exception as e:
            raise Exception(f"加载文档时出错: {str(e)}")
            
    def display_content(self, content: str) -> None:
        """显示文档内容"""
        # 创建字体tag
        self.text_widget.tag_configure('content', font=('Noto Sans SC', self.current_font_size))
        
        # 插入内容并应用tag
        self.text_widget.insert('1.0', content, 'content')
        self.text_widget.config(state='disabled')  # 设为只读
        
    def show_error(self, error_msg: str) -> None:
        """显示错误信息"""
        self.text_widget.insert('1.0', f"错误: {error_msg}")
        self.text_widget.config(state='disabled')
        
    def create_interface(self) -> None:
        """创建文档查看界面"""
        # 文档内容区域 - 直接填满整个窗口
        content_frame = tk.Frame(self.window, bg='#1a1a1a')
        content_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # 创建文本框 - 无滚动条
        self.text_widget = tk.Text(
            content_frame,
            bg='#1a1a1a',
            fg='#ffffff',
            font=('Noto Sans SC', self.current_font_size),  # 使用当前字体大小
            wrap='word',
            padx=20,
            pady=20,
            border=0,
            insertbackground='#ffffff',
            selectbackground='#404040',
            selectforeground='#ffffff'
        )
        
        # 布局 - 文本框填满整个区域
        self.text_widget.pack(expand=True, fill='both')
        
        # 设置文本框焦点，使其能响应键盘事件
        self.text_widget.focus_set()
        
        # 绑定键盘事件
        self.window.bind('<Escape>', lambda e: self.close_window())
        self.window.bind('<Control-w>', lambda e: self.close_window())
        
        # 绑定上下键滚动事件
        self.text_widget.bind('<Up>', self.scroll_up)
        self.text_widget.bind('<Down>', self.scroll_down)
        self.text_widget.bind('<Prior>', self.page_up)  # Page Up
        self.text_widget.bind('<Next>', self.page_down)  # Page Down
        self.text_widget.bind('<Home>', self.go_to_start)  # Home
        self.text_widget.bind('<End>', self.go_to_end)  # End
        
    def scroll_up(self, event: tk.Event) -> str:
        """向上滚动"""
        self.text_widget.yview_scroll(-1, "units")
        return "break"  # 阻止默认行为
        
    def scroll_down(self, event: tk.Event) -> str:
        """向下滚动"""
        self.text_widget.yview_scroll(1, "units")
        return "break"  # 阻止默认行为
        
    def page_up(self, event: tk.Event) -> str:
        """向上翻页"""
        self.text_widget.yview_scroll(-10, "units")
        return "break"
        
    def page_down(self, event: tk.Event) -> str:
        """向下翻页"""
        self.text_widget.yview_scroll(10, "units")
        return "break"
        
    def go_to_start(self, event: tk.Event) -> str:
        """跳转到文档开头"""
        self.text_widget.see("1.0")
        return "break"
        
    def go_to_end(self, event: tk.Event) -> str:
        """跳转到文档结尾"""
        self.text_widget.see("end")
        return "break"

    def close_window(self) -> None:
        """关闭窗口并显示主窗口"""
        self.window.destroy()
        # 重新显示主窗口
        self.parent.deiconify()

class MyTempoApp:
    def __init__(self) -> None:
        # Create main window first but don't show it
        self.root = tkdnd.Tk()
        self.root.withdraw()
        self.root.title("My Tempo")
        self.root.geometry("600x450")
        self.root.configure(bg='#f5f5f7')
        
        # Show loading window
        loading_window = LoadingWindow(self.root, "Loading Fonts")
        
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
        loading_window.destroy()
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
            # 处理有效的Markdown文件 - 只打开第一个文件
            try:
                DocumentViewer(self.root, valid_files[0])
                if len(valid_files) > 1:
                    messagebox.showinfo(
                        "提示",
                        f"检测到{len(valid_files)}个文件，当前只打开第一个文件：\n{os.path.basename(valid_files[0])}"
                    )
            except Exception as e:
                messagebox.showerror(
                    "打开文件失败",
                    f"无法打开文件 {os.path.basename(valid_files[0])}:\n{str(e)}"
                )
            
    def run(self) -> None:
        """Run the application"""
        self.root.mainloop()

if __name__ == '__main__':
    app = MyTempoApp()
    app.run() 