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
        self.parent = parent  # 保存父窗口引用
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
        """销毁加载窗口并将焦点返回给父窗口"""
        self.root.destroy()
        if self.parent:
            self.parent.focus_force()  # 强制将焦点返回给父窗口

class DocumentViewer:
    """文档查看器类"""
    # 版本号
    VERSION = "0.2.4"  # 添加了窗口置顶功能
    
    # 支持的字体大小
    FONT_SIZES = [10, 11, 12, 14, 16, 18, 20, 22, 24, 28, 32, 36, 48, 60, 72]
    DEFAULT_FONT_SIZE = 24

    # 滚动相关配置
    BASE_SPEED = 0.0002  # 基础速度（1x）
    SCROLL_SPEEDS = [1, 2, 3, 4, 5]  # 速度倍率列表，从1x到5x
    DEFAULT_SPEED_INDEX = 0  # 默认使用1倍速
    SCROLL_INTERVAL = 16  # 滚动更新间隔（毫秒），约60fps以实现最佳平滑效果

    # 透明度相关配置
    OPACITY_LEVELS = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]  # 从不透明到透明
    DEFAULT_OPACITY_INDEX = 5  # 默认使用50%不透明度

    def __init__(self, parent: tk.Tk, file_path: str) -> None:
        """初始化文档查看器"""
        self.parent = parent
        self.file_path = file_path
        self.current_font_size = self.DEFAULT_FONT_SIZE
        self.current_speed_index = self.DEFAULT_SPEED_INDEX  # 当前速度倍率索引
        self.current_opacity_index = self.DEFAULT_OPACITY_INDEX  # 当前透明度索引
        self.is_scrolling = False  # 是否正在滚动
        self.scroll_id = None  # 滚动定时器ID
        
        # 隐藏主窗口
        self.parent.withdraw()

        # 创建文档查看窗口
        self.window = tk.Toplevel(parent)
        self.window.title(f"My Tempo - {os.path.basename(self.file_path)}")
        self.window.geometry("900x700")
        self.window.configure(bg='#1a1a1a')
        
        # 设置窗口置顶
        self.window.attributes('-topmost', True)
        
        # 设置初始透明度
        self.window.attributes('-alpha', self.OPACITY_LEVELS[self.current_opacity_index])
        
        # 设置窗口关闭事件
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        
        # 居中显示窗口
        self.center_window()
        
        # 创建并显示加载界面
        self.loading_window = LoadingWindow(self.window, "Loading Document")
        self.window.after(100, self.load_document)

    def load_document(self) -> None:
        """加载文档内容"""
        try:
            # 更新加载状态
            self.loading_window.update_progress(1, 4, "Creating text widget...")
            
            # 创建文本框
            self.create_text_widget()
            
            # 更新加载状态
            self.loading_window.update_progress(2, 4, "Loading content...")
            
            # 加载文件内容
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 更新加载状态
            self.loading_window.update_progress(3, 4, "Rendering content...")
            
            # 设置文本内容
            self.text_widget.config(state=tk.NORMAL)  # 临时启用编辑
            self.text_widget.delete('1.0', tk.END)
            
            # 分析文本并应用适当的字体
            pos = '1.0'
            for char in content:
                if '\u4e00' <= char <= '\u9fff':  # 中文字符范围
                    self.text_widget.insert(pos, char, 'zh')
                else:
                    self.text_widget.insert(pos, char, 'en')
                pos = self.text_widget.index(f"{pos}+1c")
            
            self.text_widget.config(state=tk.DISABLED)  # 重新禁用编辑
            
            # 绑定键盘事件
            self.bind_keyboard_events()
            
            # 确保透明度设置正确
            self.window.attributes('-alpha', self.OPACITY_LEVELS[self.current_opacity_index])
            
            # 更新加载状态
            self.loading_window.update_progress(4, 4, "Complete")
            
            # 确保最小显示时间
            self.loading_window.ensure_minimum_time()
            
            # 销毁加载窗口
            self.loading_window.destroy()
            
            # 更新窗口标题
            self.update_window_title()
            
            # 设置窗口在最前面显示并将焦点设置到文本区域
            self.window.lift()
            self.window.focus_force()
            self.text_widget.focus_set()  # 将焦点设置到文本区域
            
        except Exception as e:
            messagebox.showerror("打开文件失败", f"无法打开文件 {os.path.basename(self.file_path)}:\n{str(e)}")
            self.close_window()

    def create_text_widget(self) -> None:
        """创建文本框"""
        # 创建文本框
        self.text_widget = tk.Text(
            self.window,
            font=('Noto Sans SC', self.current_font_size),  # 默认使用中文字体
            bg='#1a1a1a',  # 深色背景
            fg='#ffffff',  # 白色文字
            insertbackground='#ffffff',  # 白色光标
            wrap=tk.WORD,  # 按词换行
            padx=40,  # 左右内边距
            pady=40,  # 上下内边距
            spacing1=8,  # 段落间距
            cursor='arrow'  # 使用箭头光标
        )
        self.text_widget.pack(expand=True, fill='both')
        
        # 配置中文字体标签
        self.text_widget.tag_configure('zh', font=('Noto Sans SC', self.current_font_size))
        # 配置英文字体标签
        self.text_widget.tag_configure('en', font=('Inter', self.current_font_size))
        
        # 禁用文本编辑
        self.text_widget.config(state=tk.DISABLED)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 配置文本框的滚动
        self.text_widget.configure(yscrollcommand=scrollbar.set)

    def update_window_title(self) -> None:
        """更新窗口标题，包含文件名、字体大小、滚动速度和透明度信息"""
        speed_multiplier = self.SCROLL_SPEEDS[self.current_speed_index]
        opacity_percentage = int(self.OPACITY_LEVELS[self.current_opacity_index] * 100)
        title = f"My Tempo - {os.path.basename(self.file_path)} - Size: {self.current_font_size}px (←→) - Speed: {speed_multiplier}x (+-) - Opacity: {opacity_percentage}% (*/)"
        self.window.title(title)

    def handle_left_key(self, event: tk.Event) -> str:
        """处理左键事件"""
        self.decrease_font_size()
        return 'break'

    def handle_right_key(self, event: tk.Event) -> str:
        """处理右键事件"""
        self.increase_font_size()
        return 'break'

    def decrease_font_size(self) -> None:
        """减小字体大小"""
        if self.current_font_size > 10:
            self.current_font_size = next(size for size in reversed(self.FONT_SIZES) if size < self.current_font_size)
            self.update_font_size()

    def increase_font_size(self) -> None:
        """增加字体大小"""
        if self.current_font_size < 72:
            self.current_font_size = next(size for size in self.FONT_SIZES if size > self.current_font_size)
            self.update_font_size()

    def update_font_size(self) -> None:
        """更新字体大小"""
        if hasattr(self, 'text_widget'):
            # 保存当前滚动位置
            current_position = self.text_widget.yview()
            
            # 更新字体大小
            self.text_widget.configure(font=('Noto Sans SC', self.current_font_size))
            self.text_widget.tag_configure('zh', font=('Noto Sans SC', self.current_font_size))
            self.text_widget.tag_configure('en', font=('Inter', self.current_font_size))
            
            # 恢复滚动位置
            self.text_widget.yview_moveto(current_position[0])
            
            # 更新窗口标题
            self.update_window_title()

    def center_window(self) -> None:
        """将窗口居中显示"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def bind_keyboard_events(self) -> None:
        """绑定所有键盘事件"""
        # 禁用文本框的默认左右键绑定，并重新绑定为字体大小调整
        self.text_widget.bind('<Left>', self.handle_left_key)
        self.text_widget.bind('<Right>', self.handle_right_key)
        
        # 窗口级别的快捷键
        self.window.bind('<Escape>', lambda e: self.close_window())
        self.window.bind('<Control-w>', lambda e: self.close_window())
        
        # 滚动速度调整
        self.window.bind('<plus>', self.increase_scroll_speed)  # +键
        self.window.bind('<minus>', self.decrease_scroll_speed)  # -键

        # 透明度调整
        self.window.bind('<asterisk>', self.increase_opacity)  # *键
        self.window.bind('<slash>', self.decrease_opacity)     # /键
        
        # 文本框级别的导航键
        self.text_widget.bind('<Up>', self.scroll_up)
        self.text_widget.bind('<Down>', self.start_smooth_scroll)  # 按下时开始滚动
        self.text_widget.bind('<KeyRelease-Down>', self.stop_smooth_scroll)  # 释放时停止滚动
        self.text_widget.bind('<Prior>', self.page_up)  # Page Up
        self.text_widget.bind('<Next>', self.page_down)  # Page Down
        self.text_widget.bind('<Home>', self.go_to_start)  # Home
        self.text_widget.bind('<End>', self.go_to_end)  # End

    def scroll_up(self, event: tk.Event) -> str:
        """向上滚动"""
        self.text_widget.yview_scroll(-1, 'units')
        return 'break'  # 阻止默认的光标移动行为
        
    def scroll_down(self, event: tk.Event) -> str:
        """向下滚动"""
        self.text_widget.yview_scroll(1, 'units')
        return 'break'  # 阻止默认的光标移动行为
        
    def page_up(self, event: tk.Event) -> str:
        """向上翻页"""
        self.text_widget.yview_scroll(-1, 'pages')
        return 'break'  # 阻止默认的光标移动行为
        
    def page_down(self, event: tk.Event) -> str:
        """向下翻页"""
        self.text_widget.yview_scroll(1, 'pages')
        return 'break'  # 阻止默认的光标移动行为
        
    def go_to_start(self, event: tk.Event) -> str:
        """跳转到开头"""
        self.text_widget.yview_moveto(0)
        return 'break'  # 阻止默认的光标移动行为
        
    def go_to_end(self, event: tk.Event) -> str:
        """跳转到结尾"""
        self.text_widget.yview_moveto(1)
        return 'break'  # 阻止默认的光标移动行为

    def start_smooth_scroll(self, event: tk.Event = None) -> str:
        """开始平滑滚动"""
        if not self.is_scrolling:
            self.is_scrolling = True
            self.smooth_scroll()
        return 'break'

    def stop_smooth_scroll(self, event: tk.Event = None) -> str:
        """停止平滑滚动"""
        self.is_scrolling = False
        if self.scroll_id:
            self.window.after_cancel(self.scroll_id)
            self.scroll_id = None
        return 'break'

    def smooth_scroll(self) -> None:
        """执行平滑滚动"""
        if self.is_scrolling:
            # 获取当前滚动位置
            current_pos = self.text_widget.yview()[0]
            
            # 如果还没到底部，继续滚动
            if current_pos < 1.0:
                # 使用当前速度倍率计算实际滚动速度
                speed_multiplier = self.SCROLL_SPEEDS[self.current_speed_index]
                current_speed = self.BASE_SPEED * speed_multiplier
                self.text_widget.yview_moveto(current_pos + current_speed)
                self.scroll_id = self.window.after(self.SCROLL_INTERVAL, self.smooth_scroll)
            else:
                self.stop_smooth_scroll()

    def close_window(self) -> None:
        """关闭窗口并显示主窗口"""
        # 确保停止所有滚动
        self.stop_smooth_scroll()
        self.window.destroy()
        # 重新显示主窗口
        self.parent.deiconify()

    def increase_scroll_speed(self, event: tk.Event = None) -> str:
        """增加滚动速度"""
        if self.current_speed_index < len(self.SCROLL_SPEEDS) - 1:
            self.current_speed_index += 1
            self.update_window_title()
        return 'break'

    def decrease_scroll_speed(self, event: tk.Event = None) -> str:
        """减小滚动速度"""
        if self.current_speed_index > 0:
            self.current_speed_index -= 1
            self.update_window_title()
        return 'break'

    def increase_opacity(self, event: tk.Event = None) -> str:
        """增加不透明度"""
        if self.current_opacity_index > 0:
            self.current_opacity_index -= 1
            self.window.attributes('-alpha', self.OPACITY_LEVELS[self.current_opacity_index])
            self.update_window_title()
        return 'break'

    def decrease_opacity(self, event: tk.Event = None) -> str:
        """减小不透明度"""
        if self.current_opacity_index < len(self.OPACITY_LEVELS) - 1:
            self.current_opacity_index += 1
            self.window.attributes('-alpha', self.OPACITY_LEVELS[self.current_opacity_index])
            self.update_window_title()
        return 'break'

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
        self.root.focus_force()  # 确保主窗口获得焦点
        
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