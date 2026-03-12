#!/usr/bin/env python3
"""
Test navigation to SADP folder specifically
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_sadp_navigation():
    """Test finding and navigating to SADP folder"""
    print("🧪 Testing SADP Folder Navigation")
    print("=" * 40)
    
    from core.natural_language_parser import NaturalLanguageParser
    
    parser = NaturalLanguageParser()
    
    # Test various ways to access SADP
    test_cases = [
        "go to SADP",
        "work in folder SADP", 
        "find folder SADP",
        "navigate to SADP",
        "cd to SADP"
    ]
    
    print("Current directory:", os.getcwd())
    print()
    
    for test_input in test_cases:
        print(f"💬 Testing: '{test_input}'")
        command, confidence, suggestions = parser.parse_command(test_input)
        print(f"   🔄 Command: {command}")
        print(f"   🎯 Confidence: {confidence:.0%}")
        
        if suggestions:
            print(f"   💡 Suggestions:")
            for suggestion in suggestions[:3]:
                print(f"      {suggestion}")
        print()
    
    # Check if SADP folder exists in current directory
    print("🔍 Direct folder search:")
    sadp_paths = [
        os.path.join(os.getcwd(), "SADP"),
        os.path.join(os.path.expanduser("~"), "SADP"),
        os.path.join(os.path.expanduser("~/Desktop"), "SADP"),
        os.path.join(os.path.expanduser("~/Downloads"), "SADP"),
    ]
    
    for path in sadp_paths:
        if os.path.exists(path) and os.path.isdir(path):
            print(f"   ✅ Found SADP at: {path}")
        else:
            print(f"   ❌ Not found: {path}")
    
    # Use parser's find_folder method
    print()
    print("🔍 Using parser's find_folder method:")
    found_folders = parser.find_folder("SADP")
    if found_folders:
        print(f"   ✅ Found {len(found_folders)} SADP folder(s):")
        for folder in found_folders:
            print(f"      📁 {folder}")
    else:
        print("   ❌ No SADP folders found")

if __name__ == "__main__":
    test_sadp_navigation()
