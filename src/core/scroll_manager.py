"""
Scroll management for MyTempo document viewer.
"""

import tkinter as tk
from typing import Optional, Callable
from src.utils.constants import BASE_SPEED, SCROLL_SPEEDS, SCROLL_INTERVAL


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
        
        # Ensure speed index is within valid range
        self.current_speed_index = max(
            min(self.current_speed_index, len(SCROLL_SPEEDS) - 1), 0
        )
    
    def start_smooth_scroll(self, event: Optional[tk.Event] = None) -> str:
        """Start smooth scrolling.
        
        Args:
            event: Optional event object
            
        Returns:
            'break' to prevent default behavior
        """
        if not self.is_scrolling:
            self.is_scrolling = True
            self.smooth_scroll()
        return 'break'
    
    def stop_smooth_scroll(self, event: Optional[tk.Event] = None) -> str:
        """Stop smooth scrolling.
        
        Args:
            event: Optional event object
            
        Returns:
            'break' to prevent default behavior
        """
        self.is_scrolling = False
        if self.scroll_id:
            self.text_widget.after_cancel(self.scroll_id)
            self.scroll_id = None
        return 'break'
    
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
                self.stop_smooth_scroll()
    
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
        return 'break'
    
    def get_current_speed_multiplier(self) -> int:
        """Get current speed multiplier.
        
        Returns:
            Current speed multiplier
        """
        return SCROLL_SPEEDS[self.current_speed_index]
    
    def bind_scroll_events(self, window: tk.Tk) -> None:
        """Bind scroll events to window and text widget.
        
        Args:
            window: Main window
        """
        # Window level shortcut keys
        window.bind('<plus>', self.increase_speed)
        window.bind('<minus>', self.decrease_speed)
        
        # Text widget level navigation keys
        self.text_widget.bind('<Up>', self.scroll_up)
        self.text_widget.bind('<Down>', self.start_smooth_scroll)
        self.text_widget.bind('<KeyRelease-Down>', self.stop_smooth_scroll)
        self.text_widget.bind('<Prior>', self.page_up)
        self.text_widget.bind('<Next>', self.page_down)
        self.text_widget.bind('<Home>', self.go_to_start)
        self.text_widget.bind('<End>', self.go_to_end) 