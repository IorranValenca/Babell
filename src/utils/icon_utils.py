"""
Icon utilities for Babell
Handles loading and converting icons for the terminal window
"""

import tkinter as tk
from pathlib import Path

def set_window_icon(root_window, icon_path="assets/BABELL.png"):
    """
    Set window icon with fallback options
    """
    icon_file = Path(icon_path)
    
    if not icon_file.exists():
        return False
    
    try:
        # Method 1: Try direct iconbitmap (works with .ico files)
        if icon_file.suffix.lower() == '.ico':
            root_window.iconbitmap(str(icon_file))
            return True
    except Exception:
        pass
    
    try:
        # Method 2: Try iconphoto with PIL (works with PNG, JPG, etc.)
        from PIL import Image, ImageTk
        
        # Open and resize image if needed
        img = Image.open(icon_file)
        
        # Resize to standard icon size if too large
        if img.width > 64 or img.height > 64:
            img = img.resize((32, 32), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(img)
        root_window.iconphoto(True, photo)
        
        # Keep a reference to prevent garbage collection
        root_window._icon_photo = photo
        return True
        
    except ImportError:
        # PIL not available, try basic tkinter approach
        pass
    except Exception:
        pass
    
    try:
        # Method 3: Try with basic tkinter PhotoImage (limited formats)
        if icon_file.suffix.lower() in ['.png', '.gif']:
            photo = tk.PhotoImage(file=str(icon_file))
            root_window.iconphoto(True, photo)
            root_window._icon_photo = photo
            return True
    except Exception:
        pass
    
    # All methods failed
    return False
