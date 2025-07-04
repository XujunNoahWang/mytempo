#!/usr/bin/env python3
"""
MyTempo - A Markdown reader application.
Main entry point for the application.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app.mytempo_app import MyTempoApp

__version__ = '0.5.1'  # Fixed circular import issues and improved module structure

def main():
    """Main function to start the application."""
    app = MyTempoApp()
    app.run()

if __name__ == '__main__':
    main() 