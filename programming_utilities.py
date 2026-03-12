"""
Programming Utilities for Babell - Fixed Version
Provides enhanced programming-specific functionality
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class ProgrammingUtilities:
    """
    Enhanced utilities for programming and development tasks
    """
    
    def __init__(self):
        self.supported_languages = {
            'python': {
                'extensions': ['.py', '.pyw'],
                'runner': 'python',
                'repl': 'python',
                'package_manager': 'pip'
            },
            'javascript': {
                'extensions': ['.js', '.mjs'],
                'runner': 'node',
                'repl': 'node', 
                'package_manager': 'npm'
            }
        }
    
    def detect_project_type(self, directory: str) -> Optional[str]:
        """Detect the type of project in the given directory"""
        dir_path = Path(directory)
        
        # Check for specific files that indicate project type
        if (dir_path / 'package.json').exists():
            return 'node'
        elif (dir_path / 'requirements.txt').exists() or any(dir_path.glob("*.py")):
            return 'python'
        elif (dir_path / 'Dockerfile').exists():
            return 'docker'
        elif (dir_path / '.git').exists():
            return 'git'
        
        return None
    
    def get_smart_suggestions(self, current_dir: str, user_input: str) -> List[str]:
        """Get context-aware programming suggestions"""
        suggestions = []
        project_type = self.detect_project_type(current_dir)
        
        if project_type:
            suggestions.append(f"💡 Detected {project_type} project")
            
            # Project-specific suggestions
            if project_type == 'node':
                suggestions.extend([
                    "💡 Try: 'npm install package-name'",
                    "💡 Try: 'npm run dev'",
                    "💡 Try: 'npm run build'"
                ])
            elif project_type == 'python':
                suggestions.extend([
                    "💡 Try: 'pip install package-name'", 
                    "💡 Try: 'run python file main.py'",
                    "💡 Try: 'activate python venv'"
                ])
        
        # Keyword-based suggestions
        keywords_in_input = user_input.lower()
        if 'git' in keywords_in_input:
            suggestions.extend([
                "💡 Try: 'git status'",
                "💡 Try: 'git add all'",
                "💡 Try: 'git commit with message \"update\"'"
            ])
        elif 'create' in keywords_in_input:
            suggestions.extend([
                "💡 Try: 'create html file index'",
                "💡 Try: 'create python file main'",
                "💡 Try: 'create react app myproject'"
            ])
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def create_project_template(self, project_type: str, name: str, directory: str) -> Dict[str, str]:
        """Create a project template"""
        templates = {
            'html': {
                'index.html': f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Welcome to {name}</h1>
    <script src="script.js"></script>
</body>
</html>''',
                'style.css': f'''/* CSS for {name} */
body {{
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f5f5f5;
}}

h1 {{
    color: #333;
    text-align: center;
}}''',
                'script.js': f'''// JavaScript for {name}
console.log("Welcome to {name}!");

document.addEventListener("DOMContentLoaded", function() {{
    console.log("Page loaded successfully");
}});'''
            },
            'python': {
                'main.py': f'''#!/usr/bin/env python3
"""
{name} - A Python project
"""

def main():
    print("Welcome to {name}!")

if __name__ == "__main__":
    main()
''',
                'requirements.txt': f'''# Requirements for {name}
# Add your dependencies here
''',
                'README.md': f'''# {name}

A Python project.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```
'''
            }
        }
        
        return templates.get(project_type, {})
    
    def analyze_code_file(self, file_path: str) -> Dict[str, any]:
        """Analyze a code file and return metrics"""
        path = Path(file_path)
        if not path.exists():
            return {'error': 'File not found'}
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            analysis = {
                'file_name': path.name,
                'file_size': path.stat().st_size,
                'total_lines': len(lines),
                'non_empty_lines': len([line for line in lines if line.strip()]),
                'comment_lines': 0,
                'extension': path.suffix,
                'language': self._detect_language_from_extension(path.suffix)
            }
            
            # Count comment lines (basic detection)
            if path.suffix == '.py':
                for line in lines:
                    if line.strip().startswith('#'):
                        analysis['comment_lines'] += 1
            elif path.suffix in ['.js', '.java', '.c', '.cpp']:
                for line in lines:
                    stripped = line.strip()
                    if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
                        analysis['comment_lines'] += 1
            
            analysis['code_lines'] = analysis['non_empty_lines'] - analysis['comment_lines']
            
            return analysis
            
        except Exception as e:
            return {'error': str(e)}
    
    def _detect_language_from_extension(self, extension: str) -> str:
        """Detect programming language from file extension"""
        lang_map = {
            '.py': 'Python',
            '.js': 'JavaScript', 
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.c': 'C',
            '.cpp': 'C++',
            '.html': 'HTML',
            '.css': 'CSS'
        }
        return lang_map.get(extension, 'Unknown')
