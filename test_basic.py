#!/usr/bin/env python3
"""
Basic test to verify the application can start without errors.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_basic_imports():
    """Test basic imports without UI components."""
    print("Testing basic imports...")
    
    try:
        # Test utils
        from utils.constants import COLORS, VERSION
        print(f"✓ Constants imported: VERSION={VERSION}")
        
        # Test core
        from core.config import UserConfig
        print("✓ UserConfig imported")
        
        from core.text_processor import TextProcessor
        print("✓ TextProcessor imported")
        
        # Test font loader
        from utils.font_loader import load_fonts
        print("✓ Font loader imported")
        
        # Test UI components
        from ui.styles import StyleManager
        print("✓ StyleManager imported")
        
        from ui.loading_window import LoadingWindow
        print("✓ LoadingWindow imported")
        
        from ui.upload_interface import UploadInterface
        print("✓ UploadInterface imported")
        
        # Test app components
        from app.mytempo_app import MyTempoApp
        print("✓ MyTempoApp imported")
        
        from app.document_viewer import DocumentViewer
        print("✓ DocumentViewer imported")
        
        print("\n🎉 All imports successful! Application is ready for packaging.")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_basic_imports()
    sys.exit(0 if success else 1) 