"""
Constants used throughout the MyTempo application.
"""

# Application version
VERSION = "0.4.3"

# Font configuration
FONT_SIZES = [20, 22, 24, 28, 32, 36, 48, 60, 72]
DEFAULT_FONT_SIZE = 24

# Font families
CHINESE_FONT = "Noto Sans SC"
ENGLISH_FONT = "Inter"

# Scroll configuration
BASE_SPEED = 0.0002
SCROLL_SPEEDS = [1, 2, 3, 4, 5]
DEFAULT_SPEED_INDEX = 0
SCROLL_INTERVAL = 16  # milliseconds

# Opacity configuration
OPACITY_LEVELS = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
DEFAULT_OPACITY_INDEX = 5

# Window configuration
DEFAULT_WINDOW_WIDTH = 800
DEFAULT_WINDOW_HEIGHT = 700
MAIN_WINDOW_WIDTH = 600
MAIN_WINDOW_HEIGHT = 450

# Colors
COLORS = {
    'background': '#1a1a1a',
    'text': '#ffffff',
    'main_bg': '#f5f5f7',
    'white': '#ffffff',
    'primary': '#007AFF',
    'primary_hover': '#0056CC',
    'primary_pressed': '#004499',
    'border': '#e5e5e7',
    'text_secondary': '#86868b',
    'text_primary': '#1d1d1f',
    'highlight': '#404040',
    'horizontal_line': '#666666',
    'drop_hover': '#e3f2fd'
}

# UI configuration
PADDING = {
    'text': 40,
    'main': 30,
    'button': (20, 10)
}

# File configuration
CONFIG_FILE = "user_settings.json"
SUPPORTED_EXTENSIONS = ('.md', '.markdown')

# Loading configuration
MIN_LOADING_TIME = 1.0  # seconds
LOADING_COMPLETE_DELAY = 0.2  # seconds 