import os
from ctypes import windll
from typing import Tuple, List, Callable, Optional

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
    fonts_dir = os.path.join(os.path.dirname(__file__), 'fonts')
    
    if not os.path.exists(fonts_dir):
        print("Fonts folder not found")
        return False
    
    font_files: List[Tuple[str, str]] = []
    
    # Collect all font files
    for root, _, files in os.walk(fonts_dir):
        font_files.extend(
            (os.path.join(root, file), file)
            for file in files
            if file.endswith('.ttf')
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