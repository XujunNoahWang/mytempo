"""
Scroll management for MyTempo document viewer.
"""

import platform
import re
import subprocess
import tkinter as tk
from typing import Callable, Optional

from src.utils.constants import BASE_SPEED, SCROLL_INTERVAL, SCROLL_SPEEDS


class ScrollManager:
    """Manages document scrolling functionality"""
    
    def __init__(self, text_widget: tk.Text, config: 'UserConfig') -> None:
        """Initialize scroll manager.
        
        Args:
            text_widget: Text widget to control
            config: User configuration instance
        """
        self.text_widget = text_widget
        self.config = config
        self.is_scrolling = False
        self.scroll_id: Optional[str] = None
        self.current_speed_index = config.get("speed_index", 0)
        self.presentation_remote_detected = False
        
        # Ensure speed index is within valid range
        self.current_speed_index = max(
            min(self.current_speed_index, len(SCROLL_SPEEDS) - 1), 0
        )
        
        # Detect presentation remote
        self.detect_presentation_remote()
    
    def detect_presentation_remote(self) -> None:
        """Detect if a presentation remote is connected."""
        try:
            if platform.system() == "Windows":
                # Use PowerShell to get USB devices
                result = subprocess.run(
                    ["powershell", "Get-PnpDevice | Where-Object {$_.Class -eq 'HIDClass'} | Select-Object FriendlyName, Status"],
                    capture_output=True, text=True, timeout=5
                )
                
                if result.returncode == 0:
                    output = result.stdout.lower()
                    # Common presentation remote keywords
                    remote_keywords = [
                        'presentation', 'remote', 'clicker', 'pointer', 
                        'laser', 'wireless', 'rf', 'bluetooth', 'usb'
                    ]
                    
                    for keyword in remote_keywords:
                        if keyword in output:
                            self.presentation_remote_detected = True
                            print(f"✓ Presentation remote detected: {keyword}")
                            break
                            
            elif platform.system() == "Darwin":  # macOS
                # Use system_profiler on macOS
                result = subprocess.run(
                    ["system_profiler", "SPUSBDataType"],
                    capture_output=True, text=True, timeout=5
                )
                
                if result.returncode == 0:
                    output = result.stdout.lower()
                    remote_keywords = ['presentation', 'remote', 'clicker', 'pointer']
                    
                    for keyword in remote_keywords:
                        if keyword in output:
                            self.presentation_remote_detected = True
                            print(f"✓ Presentation remote detected: {keyword}")
                            break
                            
            elif platform.system() == "Linux":
                # Use lsusb on Linux
                result = subprocess.run(
                    ["lsusb"],
                    capture_output=True, text=True, timeout=5
                )
                
                if result.returncode == 0:
                    output = result.stdout.lower()
                    remote_keywords = ['presentation', 'remote', 'clicker', 'pointer']
                    
                    for keyword in remote_keywords:
                        if keyword in output:
                            self.presentation_remote_detected = True
                            print(f"✓ Presentation remote detected: {keyword}")
                            break
                            
        except Exception as e:
            print(f"Error detecting presentation remote: {e}")
        
        if not self.presentation_remote_detected:
            print("ℹ No presentation remote detected, using keyboard controls only")
    
    def toggle_smooth_scroll(self, event: Optional[tk.Event] = None) -> str:
        """Toggle smooth scroll on/off."""
        if not self.is_scrolling:
            self.is_scrolling = True
            self.smooth_scroll()
        else:
            self.is_scrolling = False
            if self.scroll_id:
                self.text_widget.after_cancel(self.scroll_id)
                self.scroll_id = None
        return 'break'
    
    def scroll_up(self, event: Optional[tk.Event] = None) -> str:
        """Scroll up one unit.
        
        Args:
            event: Optional event object
            
        Returns:
            'break' to prevent default behavior
        """
        self.text_widget.yview_scroll(-1, 'units')
        return 'break'
    
    def scroll_down(self, event: Optional[tk.Event] = None) -> str:
        """Scroll down one unit.
        
        Args:
            event: Optional event object
            
        Returns:
            'break' to prevent default behavior
        """
        self.text_widget.yview_scroll(1, 'units')
        return 'break'
    
    def page_up(self, event: Optional[tk.Event] = None) -> str:
        """Scroll up one page.
        
        Args:
            event: Optional event object
            
        Returns:
            'break' to prevent default behavior
        """
        self.text_widget.yview_scroll(-1, 'pages')
        return 'break'
    
    def page_down(self, event: Optional[tk.Event] = None) -> str:
        """Scroll down one page.
        
        Args:
            event: Optional event object
            
        Returns:
            'break' to prevent default behavior
        """
        self.text_widget.yview_scroll(1, 'pages')
        return 'break'
    
    def go_to_start(self, event: Optional[tk.Event] = None) -> str:
        """Jump to start of document.
        
        Args:
            event: Optional event object
            
        Returns:
            'break' to prevent default behavior
        """
        self.text_widget.yview_moveto(0)
        return 'break'
    
    def go_to_end(self, event: Optional[tk.Event] = None) -> str:
        """Jump to end of document.
        
        Args:
            event: Optional event object
            
        Returns:
            'break' to prevent default behavior
        """
        self.text_widget.yview_moveto(1)
        return 'break'
    
    def increase_speed(self, event: Optional[tk.Event] = None) -> str:
        """Increase scroll speed.
        
        Args:
            event: Optional event object
            
        Returns:
            'break' to prevent default behavior
        """
        if self.current_speed_index < len(SCROLL_SPEEDS) - 1:
            self.current_speed_index += 1
            self.config.set("speed_index", self.current_speed_index)
            # Notify parent window to update title
            if hasattr(self, 'parent_window'):
                self.parent_window.update_window_title()
        return 'break'
    
    def decrease_speed(self, event: Optional[tk.Event] = None) -> str:
        """Decrease scroll speed.
        
        Args:
            event: Optional event object
            
        Returns:
            'break' to prevent default behavior
        """
        if self.current_speed_index > 0:
            self.current_speed_index -= 1
            self.config.set("speed_index", self.current_speed_index)
            # Notify parent window to update title
            if hasattr(self, 'parent_window'):
                self.parent_window.update_window_title()
        return 'break'
    
    def get_current_speed_multiplier(self) -> int:
        """Get current speed multiplier.
        
        Returns:
            Current speed multiplier
        """
        return SCROLL_SPEEDS[self.current_speed_index]
    
    def smooth_scroll(self) -> None:
        """Execute smooth scroll step."""
        if self.is_scrolling:
            # Get current scroll position
            current_pos = self.text_widget.yview()[0]
            
            # If not at bottom, continue scrolling
            if current_pos < 1.0:
                # Use current speed multiplier to calculate actual scroll speed
                speed_multiplier = SCROLL_SPEEDS[self.current_speed_index]
                current_speed = BASE_SPEED * speed_multiplier
                self.text_widget.yview_moveto(current_pos + current_speed)
                self.scroll_id = self.text_widget.after(SCROLL_INTERVAL, self.smooth_scroll)
            else:
                self.toggle_smooth_scroll()
    
    def bind_scroll_events(self, window: tk.Tk) -> None:
        """Bind scroll events to window and text widget.
        
        Args:
            window: Main window
        """
        # Window level shortcut keys
        window.bind('<plus>', self.increase_speed)
        window.bind('<minus>', self.decrease_speed)
        
        # Text widget level navigation keys
        self.text_widget.bind('<Down>', self.scroll_down)                # 单步下移
        self.text_widget.bind('<Up>', self.scroll_up)                    # 单步上移
        self.text_widget.bind('<Next>', self.toggle_smooth_scroll)       # Page Down = 缓慢滚动
        self.text_widget.bind('<Prior>', self.scroll_up)                 # Page Up = 单步上移
        self.text_widget.bind('<Home>', self.go_to_start)
        self.text_widget.bind('<End>', self.go_to_end)
        # Down/Up为单步，Page Down为缓慢滚动，Page Up为单步上移 