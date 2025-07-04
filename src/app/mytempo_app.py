"""
Main application class for MyTempo.
"""

from typing import List

import tkinterdnd2 as tkdnd

from src.ui.loading_window import LoadingWindow
from src.ui.upload_interface import UploadInterface
from src.utils.font_loader import load_fonts


class MyTempoApp:
    """Main application class for MyTempo"""
    
    def __init__(self) -> None:
        """Initialize MyTempo application."""
        # Create main window first but don't show it
        self.root = tkdnd.Tk()
        self.root.withdraw()
        
        # Show loading window
        loading_window = LoadingWindow(self.root, "Loading Fonts")
        
        # Load fonts
        load_fonts(loading_window.update_progress)
        
        # Ensure minimum display time
        loading_window.ensure_minimum_time()
        
        # Create upload interface
        self.upload_interface = UploadInterface(self.root, self.on_file_selected)
        
        # Close loading window and show main window
        loading_window.destroy()
        self.root.deiconify()
        self.root.focus_force()
        
    def on_file_selected(self, file_paths: List[str]) -> None:
        """Handle file selection.
        
        Args:
            file_paths: List of selected file paths
        """
        if file_paths:
            # Process valid Markdown files - only open first file
            try:
                # Import DocumentViewer here to avoid circular import
                from src.app.document_viewer import DocumentViewer
                DocumentViewer(self.root, file_paths[0])
                if len(file_paths) > 1:
                    import os
                    from tkinter import messagebox
                    messagebox.showinfo(
                        "Notice",
                        f"Detected {len(file_paths)} files, currently only opening first file: \n{os.path.basename(file_paths[0])}"
                    )
            except Exception as e:
                import os
                from tkinter import messagebox
                messagebox.showerror(
                    "Failed to open file",
                    f"Cannot open file {os.path.basename(file_paths[0])}:\n{str(e)}"
                )
            
    def run(self) -> None:
        """Run the application."""
        self.root.mainloop() 