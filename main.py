#!/usr/bin/env python3
"""
MyTempo - A Markdown reader application.
Main entry point for the application.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import main

__version__ = '0.4.6'  # Project structure and codebase fully optimized

if __name__ == '__main__':
    main() 