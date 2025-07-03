"""
UI styles and theme management for MyTempo application.
"""

import tkinter as tk
from tkinter import ttk
from typing import Tuple
from src.utils.constants import COLORS, PADDING, CHINESE_FONT, ENGLISH_FONT


class StyleManager:
    """Manages UI styles and themes"""
    
    @staticmethod
    def setup_styles() -> None:
        """Set up Apple-style UI styles."""
        style = ttk.Style()
        
        # Configure Apple-style button
        style.configure('Apple.TButton',
                       background=COLORS['primary'],
                       foreground=COLORS['white'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=PADDING['button'])
        
        style.map('Apple.TButton',
                 background=[('active', COLORS['primary_hover']),
                           ('pressed', COLORS['primary_pressed'])])
    
    @staticmethod
    def get_font(is_chinese: bool = False, size: int = 12, weight: str = 'normal') -> Tuple[str, int, str]:
        """Get appropriate font configuration.
        
        Args:
            is_chinese: Whether to use Chinese font
            size: Font size
            weight: Font weight
            
        Returns:
            Font configuration tuple
        """
        return (CHINESE_FONT if is_chinese else ENGLISH_FONT, size, weight)
    
    @staticmethod
    def configure_text_tags(text_widget: tk.Text, font_size: int) -> None:
        """Configure text widget tags with appropriate fonts.
        
        Args:
            text_widget: Text widget to configure
            font_size: Base font size
        """
        # Configure basic tags
        text_widget.tag_configure('zh', font=(CHINESE_FONT, font_size))
        text_widget.tag_configure('en', font=(ENGLISH_FONT, font_size))
        
        # Configure single effect tags
        text_widget.tag_configure('zh_bold', font=(CHINESE_FONT, font_size, 'bold'))
        text_widget.tag_configure('en_bold', font=(ENGLISH_FONT, font_size, 'bold'))
        
        text_widget.tag_configure('zh_italic', font=(CHINESE_FONT, font_size, 'italic'))
        text_widget.tag_configure('en_italic', font=(ENGLISH_FONT, font_size, 'italic'))
        
        text_widget.tag_configure('zh_highlight', 
                                font=(CHINESE_FONT, font_size), 
                                background=COLORS['highlight'])
        text_widget.tag_configure('en_highlight', 
                                font=(ENGLISH_FONT, font_size), 
                                background=COLORS['highlight'])
        
        # Configure combined effect tags
        text_widget.tag_configure('zh_bold_highlight', 
                                font=(CHINESE_FONT, font_size, 'bold'), 
                                background=COLORS['highlight'])
        text_widget.tag_configure('en_bold_highlight', 
                                font=(ENGLISH_FONT, font_size, 'bold'), 
                                background=COLORS['highlight'])
        
        text_widget.tag_configure('zh_italic_highlight', 
                                font=(CHINESE_FONT, font_size, 'italic'), 
                                background=COLORS['highlight'])
        text_widget.tag_configure('en_italic_highlight', 
                                font=(ENGLISH_FONT, font_size, 'italic'), 
                                background=COLORS['highlight'])
        
        text_widget.tag_configure('zh_bold_italic', 
                                font=(CHINESE_FONT, font_size, 'bold italic'))
        text_widget.tag_configure('en_bold_italic', 
                                font=(ENGLISH_FONT, font_size, 'bold italic'))
        
        text_widget.tag_configure('zh_bold_italic_highlight', 
                                font=(CHINESE_FONT, font_size, 'bold italic'), 
                                background=COLORS['highlight'])
        text_widget.tag_configure('en_bold_italic_highlight', 
                                font=(ENGLISH_FONT, font_size, 'bold italic'), 
                                background=COLORS['highlight'])
        
        # Configure other tags
        text_widget.tag_configure('horizontal_line', 
                                font=(ENGLISH_FONT, font_size), 
                                foreground=COLORS['horizontal_line'])
        
        # Configure quote tag
        text_widget.tag_configure('zh_quote', 
                                font=(CHINESE_FONT, font_size, 'bold'), 
                                lmargin1=20, lmargin2=20)
        text_widget.tag_configure('en_quote', 
                                font=(ENGLISH_FONT, font_size, 'bold'), 
                                lmargin1=20, lmargin2=20)
        
        # Configure level title tags
        for level in range(1, 7):
            heading_size = StyleManager.get_heading_font_size(level, font_size)
            text_widget.tag_configure(f'zh_h{level}', 
                                    font=(CHINESE_FONT, heading_size, 'bold'))
            text_widget.tag_configure(f'en_h{level}', 
                                    font=(ENGLISH_FONT, heading_size, 'bold'))
    
    @staticmethod
    def get_heading_font_size(level: int, base_size: int) -> int:
        """Calculate font size based on heading level.
        
        Args:
            level: Heading level (1-6)
            base_size: Base font size
            
        Returns:
            Calculated heading font size
        """
        multipliers = {1: 2.0, 2: 1.5, 3: 1.25, 4: 1.1, 5: 1.0, 6: 0.9}
        return int(base_size * multipliers.get(level, 1.0))
    
    @staticmethod
    def configure_progress_bar_style() -> str:
        """Configure custom progress bar style.
        
        Returns:
            Style name for the progress bar
        """
        style = ttk.Style()
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=COLORS['main_bg'],
            background=COLORS['primary'],
            thickness=6
        )
        return "Custom.Horizontal.TProgressbar" 