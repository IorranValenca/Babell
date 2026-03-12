import re
import os
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

class NaturalLanguageParser:
    """
    Converts natural language commands to system commands
    """
    
    def __init__(self):
        # Try to import programming utilities
        try:
            from ..utils.programming_utilities import ProgrammingUtilities
            self.prog_utils = ProgrammingUtilities()
            self.has_prog_utils = True
        except ImportError:
            self.prog_utils = None
            self.has_prog_utils = False
        self.command_patterns = {
            # File operations
            r'(?:create|make) (?:a )?(?:new )?(?:file|document) (?:called |named )?(.+)': 'echo. > "{}"',
            r'(?:create|make) (?:a )?(?:new )?(?:folder|directory) (?:called |named )?(.+)': 'mkdir "{}"',
            r'(?:delete|remove) (?:the )?(?:file|document) (.+)': 'del "{}"',
            r'(?:delete|remove) (?:the )?(?:folder|directory) (.+)': 'rmdir /s "{}"',
            r'(?:copy|duplicate) (.+) to (.+)': 'copy "{}" "{}"',
            r'(?:move|relocate) (.+) to (.+)': 'move "{}" "{}"',
            r'(?:rename) (.+) to (.+)': 'ren "{}" "{}"',
            
            # Navigation and workspace management
            r'(?:go to|navigate to|change to|cd to) (.+)': 'smart_navigate',
            r'(?:work in|switch to|open) (?:folder|directory) (.+)': 'smart_navigate',
            r'(?:find and work in|find folder|locate folder) (.+)': 'find_and_navigate',
            r'(?:go back|go up|up one level)': 'cd ..',
            r'(?:go home|go to home)': 'cd %USERPROFILE%',
            r'(?:show|list) (?:my )?(?:projects|folders|workspaces)': 'list_projects',
            
            # Listing and viewing
            r'(?:list|show) (?:all )?(?:files|contents)': 'dir',
            r'(?:list|show) (?:all )?(?:files|contents) in (.+)': 'dir "{}"',
            r'(?:show|display|view|read) (?:the )?(?:content of |contents of )?(.+)': 'type "{}"',
            r'(?:find|search for) (.+)': 'dir /s "*{}*"',
            
            # System operations
            r'(?:show|display) (?:current )?(?:directory|folder|location)': 'cd',
            r'(?:show|display) (?:system )?(?:date|time)': 'echo %DATE% %TIME%',
            r'(?:show|display) (?:environment )?variables': 'set',
            r'(?:clear|clean) (?:the )?(?:screen|terminal)': 'cls',
            r'(?:exit|quit|close)': 'exit',
            
            # Process operations
            r'(?:kill|terminate|stop) (?:process|program) (.+)': 'taskkill /f /im "{}.exe"',
            r'(?:start|run|launch|open) (.+)': 'start "{}"',
            r'(?:show|list) (?:running )?(?:processes|programs)': 'tasklist',
            
            # Network operations
            r'(?:ping) (.+)': 'ping "{}"',
            r'(?:show|display) (?:network )?(?:connections|ports)': 'netstat -an',
            r'(?:show|display) (?:ip|network) (?:configuration|config)': 'ipconfig /all',
            
            # Text operations
            r'(?:echo|print|say) (.+)': 'echo "{}"',
            r'(?:search|grep) for (.+) in (.+)': 'findstr "{}" "{}"',
            
            # Programming & Development Operations
            # Git operations
            r'(?:git )?(?:init|initialize) (?:a )?(?:new )?(?:git )?(?:repository|repo)': 'git init',
            r'(?:git )?(?:status|check status)': 'git status',
            r'(?:git )?(?:add|stage) (?:all|everything|\.)': 'git add .',
            r'(?:git )?(?:add|stage) (.+)': 'git add "{}"',
            r'(?:git )?(?:commit) (?:with message )?["\'](.+)["\']': 'git commit -m "{}"',
            r'(?:git )?(?:push|upload) (?:to )?(?:origin|remote)?': 'git push origin main',
            r'(?:git )?(?:pull|download) (?:from )?(?:origin|remote)?': 'git pull origin main',
            r'(?:git )?(?:clone) (.+)': 'git clone "{}"',
            r'(?:git )?(?:log|history)': 'git log --oneline -10',
            r'(?:git )?(?:branch|branches)': 'git branch -a',
            r'(?:git )?(?:create branch|new branch) (.+)': 'git checkout -b "{}"',
            r'(?:git )?(?:switch to|checkout) (.+)': 'git checkout "{}"',
            r'(?:git )?(?:diff|differences)': 'git diff',
            
            # Package managers
            r'(?:npm )?(?:install|add) (.+)': 'npm install "{}"',
            r'(?:npm )?(?:install) (?:all )?(?:dependencies|deps)': 'npm install',
            r'(?:npm )?(?:run|start) (.+)': 'npm run "{}"',
            r'(?:npm )?(?:build|compile)': 'npm run build',
            r'(?:npm )?(?:test|tests)': 'npm test',
            r'(?:pip )?(?:install) (.+)': 'pip install "{}"',
            r'(?:pip )?(?:list|show) (?:packages|installed)': 'pip list',
            r'(?:pip )?(?:freeze|requirements)': 'pip freeze > requirements.txt',
            
            # Code analysis & formatting
            r'(?:count|wc) (?:lines|loc) (?:in|of) (.+)': 'powershell "(Get-Content \'{}\' | Measure-Object -Line).Lines"',
            r'(?:find|search) (?:all )?(.+) (?:files|extensions)': 'dir /s "*.{}"',
            r'(?:find|search) (.+) (?:in|inside) (?:all )?(.+) (?:files|extensions)': 'findstr /s /i "{}" "*.{}"',
            r'(?:format|prettier|beautify) (.+)': 'npx prettier --write "{}"',
            r'(?:lint|check) (.+)': 'npx eslint "{}"',
            
            # Environment & Setup
            r'(?:create|init|new) (?:node|nodejs|npm) (?:project|app)': 'npm init -y',
            r'(?:create|init|new) (?:python|py) (?:project|app|venv|virtualenv)': 'python -m venv venv',
            r'(?:activate|enable) (?:python )?(?:venv|virtualenv|environment)': 'venv\\Scripts\\activate',
            r'(?:deactivate|disable) (?:python )?(?:venv|virtualenv|environment)': 'deactivate',
            r'(?:create|new) (?:react|reactjs) (?:app|project) (.+)': 'npx create-react-app "{}"',
            r'(?:create|new) (?:vue|vuejs) (?:app|project) (.+)': 'npm create vue@latest "{}"',
            r'(?:create|new) (?:angular|ng) (?:app|project) (.+)': 'ng new "{}"',
            
            # Build & Development servers
            r'(?:start|run) (?:dev|development) (?:server)': 'npm run dev',
            r'(?:start|run) (?:local )?(?:server|serve)': 'python -m http.server 8000',
            r'(?:build|compile) (?:for )?(?:production|prod)': 'npm run build',
            r'(?:watch|live) (?:mode|reload)': 'npm run watch',
            
            # Docker operations
            r'(?:docker )?(?:build) (?:image )?(.+)': 'docker build -t "{}" .',
            r'(?:docker )?(?:run) (?:container )?(.+)': 'docker run -it "{}"',
            r'(?:docker )?(?:list|show) (?:containers|images)': 'docker ps -a',
            r'(?:docker )?(?:stop) (?:container )?(.+)': 'docker stop "{}"',
            r'(?:docker )?(?:remove|rm) (?:container )?(.+)': 'docker rm "{}"',
            
            # Code execution
            r'(?:run|execute) (?:python|py) (?:file|script) (.+)': 'python "{}"',
            r'(?:run|execute) (?:node|nodejs|js) (?:file|script) (.+)': 'node "{}"',
            r'(?:compile|build) (?:java) (.+)': 'javac "{}"',
            r'(?:run|execute) (?:java) (.+)': 'java "{}"',
            r'(?:compile|build) (?:c|cpp) (.+)': 'gcc "{}" -o "{}.exe"',
            
            # Database operations  
            r'(?:connect to|open) (?:mysql|mariadb)': 'mysql -u root -p',
            r'(?:connect to|open) (?:postgres|postgresql)': 'psql -U postgres',
            r'(?:mongo|mongodb) (?:shell|connect)': 'mongo',
            
            # File operations for development
            r'(?:create|new) (?:html|webpage) (?:file )?(.+)': 'echo "<!DOCTYPE html><html><head><title>{}</title></head><body></body></html>" > "{}.html"',
            r'(?:create|new) (?:css|stylesheet) (?:file )?(.+)': 'echo "/* CSS for {} */" > "{}.css"',
            r'(?:create|new) (?:js|javascript) (?:file )?(.+)': 'echo "// JavaScript for {}" > "{}.js"',
            r'(?:create|new) (?:py|python) (?:file )?(.+)': 'echo "#!/usr/bin/env python3" > "{}.py"',
            r'(?:create|new) (?:json) (?:file )?(.+)': 'echo "{}" > "{}.json"',
            r'(?:create|new) (?:md|markdown) (?:file )?(.+)': 'echo "# {}" > "{}.md"',
            
            # IDE & Editor operations
            r'(?:open|edit) (?:in )?(?:vscode|vs code|code) (.+)': 'code "{}"',
            r'(?:open|edit) (?:in )?(?:notepad) (.+)': 'notepad "{}"',
            r'(?:open|edit) (?:in )?(?:vim|vi) (.+)': 'vim "{}"',
            
            # Advanced programming operations
            r'(?:analyze|stats|info) (?:code )?(?:file) (.+)': 'analyze_file "{}"',
            r'(?:create|setup) (?:project|app) (?:template|scaffold) (?:for )?(.+) (?:called|named) (.+)': 'create_template "{}" "{}"',
            r'(?:detect|check|identify) (?:project|app) (?:type)': 'detect_project_type',
            r'(?:generate|create) (?:code )?(?:snippet) (?:for )?(.+) (.+)': 'generate_snippet "{}" "{}"',
            r'(?:find|search) (?:all )?(?:todo|fixme|hack) (?:comments)?': 'findstr /s /i "TODO\\|FIXME\\|HACK" "*.py" "*.js" "*.java" "*.cpp"',
            r'(?:count|measure) (?:code|loc|lines) (?:in )?(?:project)?': 'count_project_lines',
        }
        
        self.safety_patterns = [
            r'format\s+[a-z]:', r'del\s+/[sq]', r'rmdir\s+/s\s+[a-z]:\\',
            r'shutdown', r'restart', r'reboot'
        ]
    
    def parse_command(self, natural_text: str, current_dir: str = None) -> Tuple[Optional[str], float, List[str]]:
        """
        Parse natural language text into a system command
        Returns: (command, confidence, suggestions)
        """
        natural_text = natural_text.strip().lower()
        
        # Check for direct commands first
        if self._is_direct_command(natural_text):
            return natural_text, 1.0, []
        
        best_match = None
        best_confidence = 0.0
        suggestions = []
        
        for pattern, command_template in self.command_patterns.items():
            match = re.search(pattern, natural_text, re.IGNORECASE)
            if match:
                try:
                    # Calculate confidence based on match quality
                    confidence = len(match.group(0)) / len(natural_text)
                    confidence = min(confidence * 1.2, 1.0)  # Boost good matches
                    
                    if confidence > best_confidence:
                        # Format command with captured groups
                        if match.groups():
                            command = command_template.format(*match.groups())
                        else:
                            command = command_template
                        
                        # Safety check
                        if self._is_safe_command(command):
                            best_match = command
                            best_confidence = confidence
                        else:
                            suggestions.append(f"⚠️ Potentially dangerous command detected: {command}")
                
                except Exception as e:
                    suggestions.append(f"Error parsing command: {str(e)}")
        
        # Handle special commands
        if best_match in ['find_and_navigate', 'list_projects', 'smart_navigate']:
            return self.handle_special_commands(best_match, natural_text)
        
        # Generate suggestions for partial matches
        if best_confidence < 0.7:
            suggestions.extend(self._generate_suggestions(natural_text, current_dir))
        
        return best_match, best_confidence, suggestions
    
    def _is_direct_command(self, text: str) -> bool:
        """Check if text is already a valid command"""
        windows_commands = [
            'dir', 'cd', 'cls', 'echo', 'type', 'copy', 'move', 'del', 'mkdir', 
            'rmdir', 'ping', 'ipconfig', 'netstat', 'tasklist', 'taskkill'
        ]
        return any(text.startswith(cmd) for cmd in windows_commands)
    
    def _is_safe_command(self, command: str) -> bool:
        """Check if command is safe to execute"""
        return not any(re.search(pattern, command, re.IGNORECASE) for pattern in self.safety_patterns)
    
    def _generate_suggestions(self, text: str, current_dir: str = None) -> List[str]:
        """Generate helpful suggestions based on partial matches"""
        suggestions = []
        
        # Use programming utilities for smart suggestions if available
        if self.has_prog_utils and current_dir:
            prog_suggestions = self.prog_utils.get_smart_suggestions(current_dir, text)
            suggestions.extend(prog_suggestions)
        
        keywords = {
            'file': ['create file named example.txt', 'delete file example.txt', 'show file content'],
            'folder': ['create folder named MyFolder', 'go to folder', 'list folder contents'],
            'directory': ['go to directory', 'show current directory', 'create directory'],
            'list': ['list files', 'list processes', 'list network connections'],
            'show': ['show files', 'show current directory', 'show date and time'],
            'copy': ['copy file.txt to backup.txt', 'copy folder to new location'],
            'move': ['move file.txt to Documents', 'move folder to Desktop'],
            'git': ['git status', 'git add all', 'git commit with message "update"'],
            'npm': ['npm install express', 'npm run build', 'npm test'],
            'python': ['run python file script.py', 'create python venv', 'pip install requests'],
            'node': ['run node file app.js', 'create react app myapp', 'npm install'],
            'docker': ['docker build myapp', 'docker run container', 'docker list containers'],
            'create': ['create html file index', 'create python file main', 'create react app'],
            'run': ['run python script.py', 'run dev server', 'run node app.js'],
            'build': ['build for production', 'docker build image', 'compile java file'],
            'install': ['npm install package', 'pip install library', 'install dependencies'],
        }
        
        for keyword in keywords:
            if keyword in text:
                suggestions.extend([f"💡 Try: '{suggestion}'" for suggestion in keywords[keyword][:2]])
                break
        
        if not suggestions:
            suggestions.append("💡 Try commands like: 'list files', 'git status', 'npm install', 'run python file'")
        
        return suggestions[:3]  # Limit to 3 suggestions
    
    def find_folder(self, folder_name: str, search_paths: List[str] = None) -> List[str]:
        """Find folders with the given name in common locations"""
        if search_paths is None:
            search_paths = [
                os.getcwd(),  # Current directory FIRST
                os.path.expanduser("~"),  # Home directory
                os.path.expanduser("~/Desktop"),  # Desktop
                os.path.expanduser("~/Documents"),  # Documents
                "C:\\Users",  # Users directory
                "C:\\",  # C: drive root (last resort)
            ]
        
        found_folders = []
        
        for search_path in search_paths:
            try:
                if not os.path.exists(search_path):
                    continue
                
                # First check direct subdirectories (fastest)
                try:
                    for item in os.listdir(search_path):
                        item_path = os.path.join(search_path, item)
                        if os.path.isdir(item_path):
                            # Exact match (case-insensitive)
                            if item.lower() == folder_name.lower():
                                found_folders.append(os.path.abspath(item_path))
                            # Partial match
                            elif folder_name.lower() in item.lower():
                                found_folders.append(os.path.abspath(item_path))
                except PermissionError:
                    continue
                
                # If we found exact matches in current directory, prioritize them
                if search_path == os.getcwd() and found_folders:
                    break
                    
                # Only do deep search if we haven't found anything yet and it's not the C: drive
                if not found_folders and search_path != "C:\\":
                    for root, dirs, files in os.walk(search_path):
                        # Limit search depth to avoid performance issues
                        depth = root[len(search_path):].count(os.sep)
                        if depth < 2:  # Reduced depth for better performance
                            for dir_name in dirs:
                                if folder_name.lower() in dir_name.lower():
                                    found_folders.append(os.path.join(root, dir_name))
                        else:
                            dirs.clear()  # Don't recurse deeper
                        
                        # Stop if we found too many results
                        if len(found_folders) > 10:
                            break
                            
            except (PermissionError, OSError):
                continue
        
        # Remove duplicates and sort by relevance (current dir first, then exact matches)
        unique_folders = list(dict.fromkeys(found_folders))  # Preserves order
        
        # Sort: current directory first, then exact matches, then partial matches
        def sort_key(path):
            folder = os.path.basename(path)
            in_current_dir = path.startswith(os.getcwd())
            exact_match = folder.lower() == folder_name.lower()
            
            if in_current_dir and exact_match:
                return (0, 0)  # Highest priority
            elif in_current_dir:
                return (0, 1)
            elif exact_match:
                return (1, 0)
            else:
                return (1, 1)  # Lowest priority
        
        return sorted(unique_folders, key=sort_key)
    
    def get_project_folders(self) -> List[str]:
        """Get a list of likely project folders"""
        project_indicators = [
            "package.json",  # Node.js
            "requirements.txt",  # Python
            "pom.xml",  # Java Maven
            "Cargo.toml",  # Rust
            ".git",  # Git repository
            "composer.json",  # PHP
            "Gemfile",  # Ruby
            "go.mod",  # Go
            "*.sln",  # .NET solution
        ]
        
        search_paths = [
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Projects"),
            os.path.expanduser("~/Development"),
            os.path.expanduser("~/Code"),
            os.getcwd(),
        ]
        
        project_folders = []
        
        for search_path in search_paths:
            if not os.path.exists(search_path):
                continue
                
            try:
                for root, dirs, files in os.walk(search_path):
                    # Limit search depth
                    depth = root[len(search_path):].count(os.sep)
                    if depth < 3:
                        for indicator in project_indicators:
                            if indicator.startswith("*."):
                                # Handle wildcard patterns
                                extension = indicator[1:]
                                if any(f.endswith(extension) for f in files):
                                    project_folders.append(root)
                                    break
                            elif indicator in files or indicator in dirs:
                                project_folders.append(root)
                                break
                    else:
                        dirs.clear()
                        
            except (PermissionError, OSError):
                continue
        
        return sorted(list(set(project_folders)))
    
    def handle_special_commands(self, command: str, natural_text: str) -> Tuple[str, float, List[str]]:
        """Handle special commands like folder finding"""
        if command == 'smart_navigate':
            # Extract folder name from natural text
            patterns = [
                r'(?:go to|navigate to|change to|cd to) (.+)',
                r'(?:work in|switch to|open) (?:folder|directory) (.+)'
            ]
            
            folder_name = None
            for pattern in patterns:
                match = re.search(pattern, natural_text, re.IGNORECASE)
                if match:
                    folder_name = match.group(1).strip().strip('"')
                    break
            
            if folder_name:
                # First try direct path (current directory or absolute)
                direct_path = os.path.join(os.getcwd(), folder_name)
                if os.path.exists(direct_path) and os.path.isdir(direct_path):
                    return f'cd "{direct_path}"', 1.0, [f"📁 Navigating to: {direct_path}"]
                
                # Try as absolute path
                if os.path.exists(folder_name) and os.path.isdir(folder_name):
                    return f'cd "{folder_name}"', 1.0, [f"📁 Navigating to: {folder_name}"]
                
                # Search for folder using find_folder method
                found_folders = self.find_folder(folder_name)
                
                if found_folders:
                    # If only one match, navigate directly
                    if len(found_folders) == 1:
                        return f'cd "{found_folders[0]}"', 1.0, [f"📁 Navigating to: {found_folders[0]}"]
                    else:
                        # Multiple matches - show options and navigate to first one
                        suggestions = [f"📁 Found: {folder}" for folder in found_folders[:5]]
                        suggestions.insert(0, f"🔍 Found {len(found_folders)} folders matching '{folder_name}', navigating to first:")
                        return f'cd "{found_folders[0]}"', 0.8, suggestions
                else:
                    # Try basic cd command as fallback
                    return f'cd "{folder_name}"', 0.5, [f"⚠️ Folder '{folder_name}' not found in search, trying direct navigation"]
        
        elif command == 'find_and_navigate':
            # Extract folder name from natural text
            match = re.search(r'(?:find and work in|find folder|locate folder) (.+)', natural_text, re.IGNORECASE)
            if match:
                folder_name = match.group(1).strip().strip('"')
                found_folders = self.find_folder(folder_name)
                
                if found_folders:
                    # If only one match, navigate directly
                    if len(found_folders) == 1:
                        return f'cd "{found_folders[0]}"', 1.0, [f"📁 Navigating to: {found_folders[0]}"]
                    else:
                        # Multiple matches - show options
                        suggestions = [f"📁 Found: {folder}" for folder in found_folders[:5]]
                        suggestions.insert(0, f"🔍 Found {len(found_folders)} folders matching '{folder_name}':")
                        return f'echo Multiple folders found for "{folder_name}"', 0.8, suggestions
                else:
                    return f'echo Folder "{folder_name}" not found', 0.5, [f"❌ No folders found matching '{folder_name}'"]
        
        elif command == 'list_projects':
            project_folders = self.get_project_folders()
            if project_folders:
                suggestions = [f"📁 {folder}" for folder in project_folders[:10]]
                suggestions.insert(0, f"🚀 Found {len(project_folders)} project folders:")
                return 'echo Listing project folders...', 1.0, suggestions
            else:
                return 'echo No project folders found', 0.5, ["❌ No project folders detected"]
        
        return command, 0.0, []
