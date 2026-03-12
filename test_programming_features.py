#!/usr/bin/env python3
"""
Test script for Babell's enhanced programming features
"""

import sys
import os
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def test_programming_features():
    """Test the new programming-specific features"""
    print("🧪 Testing Enhanced Programming Features...")
    
    from natural_language_parser import NaturalLanguageParser
    from programming_utilities import ProgrammingUtilities
    
    parser = NaturalLanguageParser()
    prog_utils = ProgrammingUtilities()
    
    programming_test_cases = [
        "git status",
        "npm install express", 
        "run python file main.py",
        "create react app myproject",
        "docker build myapp",
        "pip install requests",
        "create html file index",
        "open in vscode app.js",
        "build for production",
        "activate python venv"
    ]
    
    print("Testing natural language parsing for programming commands:")
    print("-" * 60)
    
    for test_input in programming_test_cases:
        command, confidence, suggestions = parser.parse_command(test_input)
        print(f"Input: '{test_input}'")
        print(f"  → Command: {command}")
        print(f"  → Confidence: {confidence:.0%}")
        if suggestions:
            print(f"  → Suggestion: {suggestions[0]}")
        print()
    
    # Test project detection
    print("Testing project type detection:")
    print("-" * 40)
    
    current_dir = str(Path.cwd())
    project_type = prog_utils.detect_project_type(current_dir)
    print(f"Current directory: {current_dir}")
    print(f"Detected project type: {project_type}")
    print()
    
    # Test smart suggestions
    print("Testing smart suggestions:")
    print("-" * 30)
    
    suggestions = prog_utils.get_smart_suggestions(current_dir, "git")
    for suggestion in suggestions:
        print(f"  {suggestion}")
    print()
    
    print("✅ Programming features tests completed!")

def test_code_analysis():
    """Test code analysis features"""
    print("🧪 Testing Code Analysis...")
    
    from programming_utilities import ProgrammingUtilities
    prog_utils = ProgrammingUtilities()
    
    # Analyze existing Python files
    python_files = list(Path(".").glob("*.py"))
    
    if python_files:
        print(f"Analyzing {len(python_files)} Python files:")
        print("-" * 40)
        
        for file_path in python_files[:3]:  # Analyze first 3 files
            analysis = prog_utils.analyze_code_file(str(file_path))
            if 'error' not in analysis:
                print(f"📄 {analysis['file_name']}")
                print(f"   Language: {analysis['language']}")
                print(f"   Total lines: {analysis['total_lines']}")
                print(f"   Code lines: {analysis['code_lines']}")
                print(f"   Comment lines: {analysis['comment_lines']}")
                print(f"   File size: {analysis['file_size']} bytes")
                print()
    
    print("✅ Code analysis tests completed!")

def test_templates():
    """Test project template generation"""
    print("🧪 Testing Project Templates...")
    
    from programming_utilities import ProgrammingUtilities
    prog_utils = ProgrammingUtilities()
    
    templates = ['html', 'python', 'node']
    
    for template_type in templates:
        print(f"Testing {template_type} template:")
        template_files = prog_utils.create_project_template(template_type, "TestProject", ".")
        
        for filename, content in template_files.items():
            print(f"  📄 {filename} ({len(content)} chars)")
        print()
    
    print("✅ Template tests completed!")

def main():
    """Run all enhanced programming tests"""
    print("🚀 Babell Enhanced Programming Features - Test Suite")
    print("=" * 60)
    
    try:
        test_programming_features()
        print()
        
        test_code_analysis()
        print()
        
        test_templates()
        print()
        
        print("🎉 All enhanced programming tests completed!")
        print()
        print("🔥 Babell now supports advanced programming commands!")
        print("Try these in the terminal:")
        print("  • 'git status'")
        print("  • 'npm install express'") 
        print("  • 'create react app myproject'")
        print("  • 'docker build myapp'")
        print("  • 'run python file main.py'")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
