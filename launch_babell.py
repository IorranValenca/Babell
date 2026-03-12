#!/usr/bin/env python3
"""
Babell Launcher - Double-click friendly version
This version ensures the terminal stays open and handles errors gracefully.
"""

import sys
import os
import traceback
from pathlib import Path

def main():
    """Main launcher with enhanced error handling"""
    try:
        print("=" * 60)
        print("🚀 BABELL - Natural Language Terminal")
        print("=" * 60)
        print()
        
        # Add src directory to Python path
        script_dir = Path(__file__).parent
        src_path = script_dir / "src"
        
        if not src_path.exists():
            print("❌ ERROR: src directory not found!")
            print(f"Looking for: {src_path}")
            print("Make sure you're running this from the Babell project folder.")
            input("\nPress Enter to exit...")
            return
            
        sys.path.insert(0, str(src_path))
        
        print("📁 Loading Babell modules...")
        
        # Import and run the terminal
        from core.natural_language_terminal import NaturalLanguageTerminal
        
        print("✅ Modules loaded successfully!")
        print("🎯 Starting Babell interface...")
        print()
        
        terminal = NaturalLanguageTerminal()
        terminal.run()
        
    except ImportError as e:
        print("❌ IMPORT ERROR:")
        print(f"   {e}")
        print()
        print("🔧 Possible solutions:")
        print("   1. Make sure all files are in the correct folders")
        print("   2. Check that the src/core/ directory exists")
        print("   3. Verify Python 3.7+ is installed")
        print()
        traceback.print_exc()
        input("\nPress Enter to exit...")
        
    except KeyboardInterrupt:
        print("\n👋 Babell terminated by user (Ctrl+C)")
        print("Goodbye!")
        
    except Exception as e:
        print("❌ UNEXPECTED ERROR:")
        print(f"   {e}")
        print()
        print("🔧 Debug information:")
        traceback.print_exc()
        print()
        print("Please report this error if it persists.")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        input("Press Enter to exit...")
