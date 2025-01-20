import sys
import os
from setup import setup_logging
from main import ExcelController

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    # Setup logging
    setup_logging()
    
    # Start application
    app = ExcelController()
    app.run() 