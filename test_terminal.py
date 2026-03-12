#!/usr/bin/env python3
"""
Test script for Natural Language Terminal components
"""

import sys
import os
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def test_parser():
    """Test the natural language parser"""
    print("🧪 Testing Natural Language Parser...")
    
    from natural_language_parser import NaturalLanguageParser
    parser = NaturalLanguageParser()
    
    test_cases = [
        "create a file called test.txt",
        "list all files", 
        "go to Documents folder",
        "show the content of README.md",
        "delete the file old.txt",
        "copy important.doc to backup.doc"
    ]
    
    for test_input in test_cases:
        command, confidence, suggestions = parser.parse_command(test_input)
        print(f"Input: '{test_input}'")
        print(f"  → Command: {command}")
        print(f"  → Confidence: {confidence:.0%}")
        if suggestions:
            print(f"  → Suggestions: {suggestions[0]}")
        print()
    
    print("✅ Parser tests completed!")

def test_executor():
    """Test the command executor"""
    print("🧪 Testing Command Executor...")
    
    from command_executor import CommandExecutor
    executor = CommandExecutor()
    
    # Test safe commands
    test_commands = [
        "echo Hello World",
        "cd",  # Show current directory
        "dir /?"  # Help for dir command
    ]
    
    for command in test_commands:
        print(f"Executing: {command}")
        result = executor.execute_command(command)
        if result['success']:
            print(f"  ✅ Success: {result['output'][:50]}...")
        else:
            print(f"  ❌ Error: {result['error']}")
        print()
    
    print("✅ Executor tests completed!")

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing Module Imports...")
    
    try:
        import tkinter as tk
        print("  ✅ tkinter imported successfully")
    except ImportError as e:
        print(f"  ❌ tkinter import failed: {e}")
        return False
    
    try:
        from natural_language_parser import NaturalLanguageParser
        print("  ✅ NaturalLanguageParser imported successfully")
    except ImportError as e:
        print(f"  ❌ NaturalLanguageParser import failed: {e}")
        return False
    
    try:
        from command_executor import CommandExecutor  
        print("  ✅ CommandExecutor imported successfully")
    except ImportError as e:
        print(f"  ❌ CommandExecutor import failed: {e}")
        return False
    
    try:
        from natural_language_terminal import NaturalLanguageTerminal
        print("  ✅ NaturalLanguageTerminal imported successfully")
    except ImportError as e:
        print(f"  ❌ NaturalLanguageTerminal import failed: {e}")
        return False
    
    print("✅ All imports successful!")
    return True

def main():
    """Run all tests"""
    print("🚀 Babell - Test Suite")
    print("=" * 50)
    
    # Test imports first
    if not test_imports():
        print("❌ Import tests failed. Please check your Python installation.")
        return
    
    print()
    
    # Test parser
    try:
        test_parser()
    except Exception as e:
        print(f"❌ Parser test failed: {e}")
    
    print()
    
    # Test executor
    try:
        test_executor()
    except Exception as e:
        print(f"❌ Executor test failed: {e}")
    
    print()
    print("🎉 Test suite completed!")
    print()
    print("To start Babell, run:")
    print("  python natural_language_terminal.py")
    print("or double-click:")
    print("  run_terminal.bat")

if __name__ == "__main__":
    main()
