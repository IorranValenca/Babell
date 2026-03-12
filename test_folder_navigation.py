#!/usr/bin/env python3
"""
Test the new folder navigation features
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_folder_navigation():
    """Test folder finding and navigation features"""
    print("🧪 Testing Enhanced Folder Navigation Features")
    print("=" * 50)
    
    from core.natural_language_parser import NaturalLanguageParser
    
    parser = NaturalLanguageParser()
    
    # Test cases for folder navigation
    test_cases = [
        "work in folder Documents",
        "find folder Babell",
        "find and work in Desktop", 
        "locate folder Projects",
        "switch to folder Downloads",
        "show my projects",
        "list my workspaces",
        "go to Desktop folder"
    ]
    
    print("Testing natural language folder commands:")
    print("-" * 40)
    
    for test_input in test_cases:
        command, confidence, suggestions = parser.parse_command(test_input)
        print(f"💬 Input: '{test_input}'")
        print(f"   🔄 Command: {command}")
        print(f"   🎯 Confidence: {confidence:.0%}")
        
        if suggestions:
            print(f"   💡 Suggestions:")
            for suggestion in suggestions[:3]:
                print(f"      {suggestion}")
        print()
    
    # Test folder finding directly
    print("Testing direct folder finding:")
    print("-" * 30)
    
    test_folders = ["Desktop", "Documents", "Downloads", "Babell"]
    for folder_name in test_folders:
        print(f"🔍 Searching for '{folder_name}':")
        found = parser.find_folder(folder_name)
        if found:
            for path in found[:3]:  # Show first 3 matches
                print(f"   📁 {path}")
        else:
            print(f"   ❌ No folders found")
        print()
    
    # Test project detection
    print("Testing project folder detection:")
    print("-" * 35)
    
    projects = parser.get_project_folders()
    if projects:
        print(f"🚀 Found {len(projects)} project folders:")
        for project in projects[:5]:  # Show first 5
            print(f"   📁 {project}")
    else:
        print("❌ No project folders detected")
    
    print()
    print("✅ Folder navigation tests completed!")

if __name__ == "__main__":
    test_folder_navigation()
