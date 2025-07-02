import os
from ctypes import windll
from typing import Tuple, List

def add_font_resource(font_path: str) -> int:
    """在Windows中注册字体文件
    
    Args:
        font_path: 字体文件的完整路径
        
    Returns:
        int: 成功返回非零值，失败返回0
    """
    return windll.gdi32.AddFontResourceW(font_path)

def load_fonts() -> bool:
    """加载fonts文件夹中的字体文件
    
    Returns:
        bool: 是否成功加载至少一个字体
    """
    fonts_dir = os.path.join(os.path.dirname(__file__), 'fonts')
    
    if not os.path.exists(fonts_dir):
        print("未找到fonts文件夹")
        return False
    
    font_files: List[Tuple[str, str]] = []
    
    # 收集所有字体文件
    for root, _, files in os.walk(fonts_dir):
        font_files.extend(
            (os.path.join(root, file), file)
            for file in files
            if file.endswith('.ttf')
        )
    
    if not font_files:
        print("fonts文件夹中未找到字体文件")
        return False
    
    # 注册字体
    loaded_count = 0
    for font_path, filename in font_files:
        try:
            if add_font_resource(font_path):
                print(f"✓ 加载{os.path.basename(os.path.dirname(font_path))}字体: {filename}")
                loaded_count += 1
            else:
                print(f"✗ 加载失败: {filename}")
        except Exception as e:
            print(f"✗ 加载出错: {filename} - {str(e)}")
    
    if loaded_count > 0:
        print("字体加载完成，无需解压到磁盘")
        return True
    
    print("未能加载任何字体文件")
    return False 