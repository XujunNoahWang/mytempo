import os
from ctypes import windll
from typing import Tuple, List, Callable, Optional

def get_fonts_dir():
    """Get fonts directory path"""
    current = os.path.abspath(__file__)
    dir_path = os.path.dirname(current)
    
    # Look for fonts directory in the project structure
    while True:
        # Check for src/assets/fonts
        fonts_path = os.path.join(dir_path, 'assets', 'fonts')
        if os.path.isdir(fonts_path):
            return fonts_path
        
        # Check for fonts in current directory (backward compatibility)
        fonts_path = os.path.join(dir_path, 'fonts')
        if os.path.isdir(fonts_path):
            return fonts_path
            
        parent = os.path.dirname(dir_path)
        if parent == dir_path:
            break
        dir_path = parent
    return None

FONTS_DIR = get_fonts_dir()

def add_font_resource(font_path: str) -> int:
    """Register font file in Windows
    
    Args:
        font_path: Full path to the font file
        
    Returns:
        int: Non-zero on success, 0 on failure
    """
    return windll.gdi32.AddFontResourceW(font_path)

def load_fonts(progress_callback: Optional[Callable[[int, int, str], None]] = None) -> bool:
    """Load font files from the fonts folder
    
    Args:
        progress_callback: Progress callback function with parameters (current, total, font_name)
    
    Returns:
        bool: Whether at least one font was loaded successfully
    """
    if not FONTS_DIR:
        print("Fonts folder not found")
        return False
    
    font_files: List[Tuple[str, str]] = []
    
    # Collect all font files
    for root, _, files in os.walk(FONTS_DIR):
        font_files.extend(
            (os.path.join(root, file), file)
            for file in files if file.lower().endswith('.ttf')
        )
    
    if not font_files:
        print("No font files found in fonts folder")
        return False
    
    # Register fonts
    total_fonts = len(font_files)
    loaded_count = 0
    
    for index, (font_path, filename) in enumerate(font_files, 1):
        try:
            if add_font_resource(font_path):
                font_type = "Inter" if "Inter" in font_path else "NotoSansSC" if "NotoSansSC" in font_path else "static"
                print(f"✓ Loaded {font_type} font: {filename}")
                loaded_count += 1
                
                if progress_callback:
                    progress_callback(index, total_fonts, filename)
            else:
                print(f"✗ Failed to load: {filename}")
        except Exception as e:
            print(f"✗ Error loading: {filename} - {str(e)}")
    
    if loaded_count > 0:
        print("Font loading completed, no disk extraction needed")
        return True
    
    print("Failed to load any font files")
    return False 