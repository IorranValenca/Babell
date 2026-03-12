#!/usr/bin/env python3
"""
Babell - Natural Language Terminal
Main entry point for the application.
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Main entry point for Babell terminal"""
    try:
        from core.natural_language_terminal import NaturalLanguageTerminal
        
        print("Starting Babell - Natural Language Terminal...")
        terminal = NaturalLanguageTerminal()
        terminal.run()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure all dependencies are installed.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nBabell terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
