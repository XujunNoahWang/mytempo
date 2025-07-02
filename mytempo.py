import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
import markdown
from tkinter import font
import os
from tkinterdnd2 import DND_FILES, TkinterDnD

class FileUploadWindow(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        
        # 设置窗口
        self.title("MyTempo - 文件上传")
        self.geometry("500x300")
        
        # 创建拖放区域
        self.frame = ctk.CTkFrame(self, width=400, height=200)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.label = ctk.CTkLabel(self.frame, text="拖拽或点击选择MD文件", font=("Microsoft YaHei UI", 16))
        self.label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        
        self.button = ctk.CTkButton(self.frame, text="选择文件", command=self.open_file)
        self.button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        
        # 绑定拖放事件
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.handle_drop)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md")])
        if file_path:
            self.process_file(file_path)

    def handle_drop(self, event):
        file_path = event.data
        # 在Windows系统中，移除文件路径的大括号和引号
        file_path = file_path.strip('{}').strip('"')
        
        if file_path.lower().endswith('.md'):
            self.process_file(file_path)
        else:
            messagebox.showerror("错误", "请选择MD文件")

    def process_file(self, file_path):
        self.withdraw()  # 隐藏当前窗口
        TextDisplayWindow(file_path)

class TextDisplayWindow(ctk.CTkToplevel):
    def __init__(self, file_path):
        super().__init__()
        
        # 设置窗口
        self.title("MyTempo - 文本显示")
        self.geometry("700x600")
        self.attributes('-alpha', 0.6)  # 设置透明度
        self.configure(bg='black')  # 设置背景颜色为黑色
        
        # 创建文本显示区域
        self.text_widget = ctk.CTkTextbox(
            self,
            font=("Microsoft YaHei UI", 24),
            text_color="white",
            fg_color="black",  # 文本框背景色
            border_width=0
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        
        # 加载并显示文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            html_content = markdown.markdown(content)
            self.text_widget.insert('1.0', content)
        
        self.text_widget.configure(state="disabled")  # 设置为只读
        
        # 滚动相关变量
        self.is_scrolling = False
        self.scroll_speed = 0.0005  # 调整这个值可以改变滚动速度
        self.scroll_timer = None
        
        # 绑定按键事件
        self.bind('<KeyPress-Down>', self.start_scroll)
        self.bind('<KeyRelease-Down>', self.stop_scroll)
        
        # 显示窗口
        self.deiconify()
        self.lift()
        self.focus_force()
        
        # 允许调整窗口大小
        self.resizable(True, True)

    def start_scroll(self, event):
        if not self.is_scrolling:  # 只在第一次按下时启动滚动
            self.is_scrolling = True
            self.scroll_text()

    def stop_scroll(self, event):
        self.is_scrolling = False
        if self.scroll_timer:
            self.after_cancel(self.scroll_timer)
            self.scroll_timer = None

    def scroll_text(self):
        if self.is_scrolling:
            current_position = self.text_widget.yview()[0]
            if current_position < 1.0:  # 如果还没有滚动到底部
                self.text_widget.yview_moveto(current_position + self.scroll_speed)
                self.scroll_timer = self.after(20, self.scroll_text)  # 每20毫秒更新一次

if __name__ == "__main__":
    app = FileUploadWindow()
    app.mainloop() 