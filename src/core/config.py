"""
Configuration management for MyTempo application.
"""

import json
import os
from typing import Dict, Any, Optional
from ..utils.constants import (
    DEFAULT_FONT_SIZE, DEFAULT_SPEED_INDEX, DEFAULT_OPACITY_INDEX,
    DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT, CONFIG_FILE
)


class UserConfig:
    """User configuration management class"""
    
    def __init__(self, config_file: str = CONFIG_FILE) -> None:
        """Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file
        self.default_settings = {
            "font_size": DEFAULT_FONT_SIZE,
            "speed_index": DEFAULT_SPEED_INDEX,
            "opacity_index": DEFAULT_OPACITY_INDEX,
            "window_width": DEFAULT_WINDOW_WIDTH,
            "window_height": DEFAULT_WINDOW_HEIGHT
        }
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from config file.
        
        Returns:
            Dictionary containing user settings with defaults merged
        """
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
        """Save settings to config file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get setting value.
        
        Args:
            key: Setting key
            default: Default value if key doesn't exist
            
        Returns:
            Setting value or default
        """
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set value and save to file.
        
        Args:
            key: Setting key
            value: Setting value
        """
        self.settings[key] = value
        self.save_settings()
    
    def update_multiple(self, updates: Dict[str, Any]) -> None:
        """Batch update settings.
        
        Args:
            updates: Dictionary of settings to update
        """
        self.settings.update(updates)
        self.save_settings()
    
    def reset_to_defaults(self) -> None:
        """Reset all settings to default values."""
        self.settings = self.default_settings.copy()
        self.save_settings() 