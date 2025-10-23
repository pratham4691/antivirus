#!/usr/bin/env python3
"""
Standalone Desktop Application for Futuristic Antivirus System
Run this file directly to launch the desktop GUI.
"""

import sys
import os

# Add the current directory to Python path so we can import our modules
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from src.desktop_gui import main
    main()
except ImportError as e:
    print(f"Error importing desktop GUI: {e}")
    print("Make sure all dependencies are installed:")
    print("pip install PyQt6 psutil scikit-learn requests watchdog flask docker numpy pandas joblib cryptography")
    input("Press Enter to exit...")
except Exception as e:
    print(f"Error running desktop application: {e}")
    input("Press Enter to exit...")
