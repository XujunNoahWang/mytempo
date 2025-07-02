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
        
        # Set up window
        self.title("MyTempo - File Upload")
        self.geometry("500x300")
        
        # Create drop zone
        self.frame = ctk.CTkFrame(self, width=400, height=200)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.label = ctk.CTkLabel(self.frame, text="Drag & Drop or Click to Select MD File", font=("Microsoft YaHei UI", 16))
        self.label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        
        self.button = ctk.CTkButton(self.frame, text="Select File", command=self.open_file)
        self.button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        
        # Bind drag and drop events
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.handle_drop)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md")])
        if file_path:
            self.process_file(file_path)

    def handle_drop(self, event):
        file_path = event.data
        # Remove curly braces from file path on Windows
        file_path = file_path.strip('{}').strip('"')
        
        if file_path.lower().endswith('.md'):
            self.process_file(file_path)
        else:
            messagebox.showerror("Error", "Please select a Markdown file")

    def process_file(self, file_path):
        self.withdraw()  # Hide current window
        TextDisplayWindow(file_path)

class TextDisplayWindow(ctk.CTkToplevel):
    def __init__(self, file_path):
        super().__init__()
        
        # Set up window
        self.title("MyTempo - Text Display")
        self.geometry("700x600")
        self.attributes('-alpha', 0.6)  # Set transparency
        self.configure(bg='black')  # Set background color to black
        
        # Create text display area
        self.text_widget = ctk.CTkTextbox(
            self,
            font=("Microsoft YaHei UI", 24),
            text_color="white",
            fg_color="black",  # Text box background color
            border_width=0
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Load and display file content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            html_content = markdown.markdown(content)
            self.text_widget.insert('1.0', content)
        
        self.text_widget.configure(state="disabled")  # Set to read-only
        
        # Scrolling variables
        self.is_scrolling = False
        self.scroll_speed = 0.0005  # Adjust this value to change scroll speed
        self.scroll_timer = None
        
        # Bind key events
        self.bind('<KeyPress-Down>', self.start_scroll)
        self.bind('<KeyRelease-Down>', self.stop_scroll)
        
        # Show window
        self.deiconify()
        self.lift()
        self.focus_force()
        
        # Allow window resizing
        self.resizable(True, True)

    def start_scroll(self, event):
        if not self.is_scrolling:  # Only start scrolling on first press
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
            if current_position < 1.0:  # If not at the bottom
                self.text_widget.yview_moveto(current_position + self.scroll_speed)
                self.scroll_timer = self.after(20, self.scroll_text)  # Update every 20ms

if __name__ == "__main__":
    app = FileUploadWindow()
    app.mainloop() 