"""
Advanced Natural Language Parser with AI Integration Support
This module provides enhanced natural language understanding capabilities.
"""

import re
import json
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from pathlib import Path

class AdvancedNLParser:
    """
    Enhanced natural language parser with AI model support (future integration)
    """
    
    def __init__(self, use_ai_model: bool = False):
        self.use_ai_model = use_ai_model
        self.context_history = []
        self.user_preferences = self.load_user_preferences()
        
        # Enhanced command patterns with context awareness
        self.command_patterns = {
            # File operations with enhanced patterns
            r'(?:create|make|new) (?:a )?(?:new )?(?:empty )?(?:file|document|txt file|text file) (?:called |named |with name )?["\']?([^"\']+)["\']?': 'echo. > "{}"',
            r'(?:create|make|new) (?:a )?(?:new )?(?:folder|directory|dir) (?:called |named |with name )?["\']?([^"\']+)["\']?': 'mkdir "{}"',
            r'(?:delete|remove|erase|del) (?:the )?(?:file|document) ["\']?([^"\']+)["\']?': 'del "{}"',
            r'(?:delete|remove|erase) (?:the )?(?:folder|directory|dir) ["\']?([^"\']+)["\']?': 'rmdir /s /q "{}"',
            r'(?:copy|duplicate|cp) ["\']?([^"\']+)["\']? (?:to|into|→) ["\']?([^"\']+)["\']?': 'copy "{}" "{}"',
            r'(?:move|relocate|mv) ["\']?([^"\']+)["\']? (?:to|into|→) ["\']?([^"\']+)["\']?': 'move "{}" "{}"',
            r'(?:rename|ren) ["\']?([^"\']+)["\']? (?:to|as|→) ["\']?([^"\']+)["\']?': 'ren "{}" "{}"',
            
            # Enhanced navigation patterns
            r'(?:go to|navigate to|change to|cd to|open) (?:the )?(?:folder |directory |dir )?["\']?([^"\']+)["\']?': 'cd "{}"',
            r'(?:go back|go up|up|back|parent directory|\.\.)': 'cd ..',
            r'(?:go home|home|user folder|profile)': 'cd %USERPROFILE%',
            r'(?:go to desktop|desktop)': 'cd %USERPROFILE%\\Desktop',
            r'(?:go to documents|documents)': 'cd %USERPROFILE%\\Documents',
            r'(?:go to downloads|downloads)': 'cd %USERPROFILE%\\Downloads',
            
            # Enhanced listing and viewing
            r'(?:list|show|ls|dir) (?:all )?(?:files|contents|items)(?:\s+in\s+["\']?([^"\']*)["\']?)?': 'dir{}',
            r'(?:show|display|view|read|cat|type) (?:the )?(?:content of |contents of |file )?["\']?([^"\']+)["\']?': 'type "{}"',
            r'(?:find|search|locate) ["\']?([^"\']+)["\']?(?:\s+in\s+["\']?([^"\']*)["\']?)?': 'dir{} /s "*{}*"',
            r'(?:size of|how big is) ["\']?([^"\']+)["\']?': 'dir "{}" /s',
            
            # Enhanced system operations
            r'(?:show|display|print|pwd) (?:current )?(?:directory|folder|location|path)': 'cd',
            r'(?:show|display|print) (?:current )?(?:date|time)': 'echo %DATE% %TIME%',
            r'(?:show|display|list) (?:environment )?(?:variables|env)': 'set',
            r'(?:clear|clean|cls) (?:the )?(?:screen|terminal|console)': 'cls',
            r'(?:exit|quit|close|bye)': 'exit',
            r'(?:help|\\?)': 'help',
            
            # Process operations with enhanced patterns  
            r'(?:kill|terminate|stop|end) (?:process|program|app|application) ["\']?([^"\']+)["\']?': 'taskkill /f /im "{}.exe"',
            r'(?:start|run|launch|open|execute) ["\']?([^"\']+)["\']?': 'start "{}"',
            r'(?:show|list|display) (?:all )?(?:running )?(?:processes|programs|tasks|apps)': 'tasklist',
            
            # Network operations with enhanced patterns
            r'(?:ping|test connection to) ["\']?([^"\']+)["\']?': 'ping "{}"',
            r'(?:show|display|list) (?:network )?(?:connections|ports|netstat)': 'netstat -an',
            r'(?:show|display) (?:ip|network|net) (?:configuration|config|info)': 'ipconfig /all',
            r'(?:flush|clear) (?:dns|dns cache)': 'ipconfig /flushdns',
            
            # Text and content operations
            r'(?:echo|print|say|output) ["\']?([^"\']+)["\']?': 'echo "{}"',
            r'(?:search|grep|find text) ["\']?([^"\']+)["\']? (?:in|inside) ["\']?([^"\']+)["\']?': 'findstr "{}" "{}"',
            r'(?:count lines in|line count of|wc) ["\']?([^"\']+)["\']?': 'find /c /v "" "{}"',
            
            # Archive operations
            r'(?:compress|zip) ["\']?([^"\']+)["\']? (?:to|as) ["\']?([^"\']+)["\']?': 'powershell Compress-Archive "{}" "{}"',
            r'(?:extract|unzip) ["\']?([^"\']+)["\']?(?:\s+to\s+["\']?([^"\']*)["\']?)?': 'powershell Expand-Archive "{}" {}',
            
            # Git operations (if git is available)
            r'(?:git )?(?:status|git status)': 'git status',
            r'(?:git )?(?:add|stage) (?:all|everything|\.)': 'git add .',
            r'(?:git )?(?:add|stage) ["\']?([^"\']+)["\']?': 'git add "{}"',
            r'(?:git )?(?:commit) ["\']?([^"\']+)["\']?': 'git commit -m "{}"',
            r'(?:git )?(?:push)': 'git push',
            r'(?:git )?(?:pull)': 'git pull',
        }
        
        # Context-aware patterns (consider previous commands)
        self.contextual_patterns = {
            'after_cd': {
                r'(?:list|show|ls)': 'dir',
                r'(?:files|contents)': 'dir',
            },
            'after_create': {
                r'(?:edit|open) (?:it|that|the file)': 'notepad "{last_file}"',
                r'(?:show|view) (?:it|that|the file)': 'type "{last_file}"',
            }
        }
        
        # Advanced safety patterns
        self.danger_patterns = [
            r'format\s+[a-z]:', r'del\s+/[sq]', r'rmdir\s+/s\s+[a-z]:\\',
            r'shutdown', r'restart', r'reboot', r'rd\s+/s', r'deltree',
            r'reg\s+delete', r'bcdedit', r'diskpart'
        ]
        
        # Confidence boosters
        self.confidence_boosters = {
            'exact_match': 0.3,
            'multiple_keywords': 0.2,
            'context_match': 0.15,
            'user_preference': 0.1
        }
    
    def parse_advanced(self, natural_text: str, context: Dict[str, Any] = None) -> Tuple[Optional[str], float, List[str], Dict[str, Any]]:
        """
        Advanced parsing with context awareness and AI integration
        Returns: (command, confidence, suggestions, metadata)
        """
        natural_text = natural_text.strip()
        original_text = natural_text
        natural_text_lower = natural_text.lower()
        
        # Initialize metadata
        metadata = {
            'original_input': original_text,
            'parsing_method': 'pattern_matching',
            'timestamp': datetime.now().isoformat(),
            'context_used': bool(context)
        }
        
        # Check for direct commands first
        if self._is_direct_command(natural_text_lower):
            return natural_text, 1.0, [], {**metadata, 'parsing_method': 'direct_command'}
        
        # Try AI model if available (placeholder for future implementation)
        if self.use_ai_model:
            ai_result = self._try_ai_parsing(natural_text, context)
            if ai_result:
                return ai_result
        
        # Pattern matching with context awareness
        best_match = None
        best_confidence = 0.0
        suggestions = []
        
        # Try contextual patterns first
        if context and context.get('last_command_type'):
            contextual_match = self._try_contextual_patterns(natural_text_lower, context)
            if contextual_match:
                command, confidence = contextual_match
                if confidence > best_confidence:
                    best_match = command
                    best_confidence = confidence
                    metadata['parsing_method'] = 'contextual'
        
        # Try regular patterns
        for pattern, command_template in self.command_patterns.items():
            match = re.search(pattern, natural_text_lower, re.IGNORECASE)
            if match:
                try:
                    confidence = self._calculate_confidence(match, natural_text_lower, pattern)
                    
                    if confidence > best_confidence:
                        command = self._format_command(command_template, match, context)
                        
                        if self._is_safe_command(command):
                            best_match = command
                            best_confidence = confidence
                        else:
                            suggestions.append(f"⚠️ Potentially dangerous command: {command}")
                
                except Exception as e:
                    suggestions.append(f"Error parsing pattern: {str(e)}")
        
        # Generate enhanced suggestions
        if best_confidence < 0.7:
            suggestions.extend(self._generate_enhanced_suggestions(natural_text_lower, context))
        
        # Update user preferences based on successful matches
        if best_match and best_confidence > 0.8:
            self._update_user_preferences(original_text, best_match)
        
        return best_match, best_confidence, suggestions, metadata
    
    def _calculate_confidence(self, match, text: str, pattern: str) -> float:
        """Calculate confidence score with multiple factors"""
        base_confidence = len(match.group(0)) / len(text)
        
        # Apply confidence boosters
        confidence = base_confidence
        
        # Exact match boost
        if match.group(0).lower() == text:
            confidence += self.confidence_boosters['exact_match']
        
        # Multiple keywords boost
        keywords = ['file', 'folder', 'create', 'delete', 'copy', 'move', 'list', 'show']
        keyword_count = sum(1 for keyword in keywords if keyword in text)
        if keyword_count > 1:
            confidence += self.confidence_boosters['multiple_keywords']
        
        # User preference boost
        if text in self.user_preferences.get('frequent_commands', []):
            confidence += self.confidence_boosters['user_preference']
        
        return min(confidence, 1.0)
    
    def _format_command(self, template: str, match, context: Dict[str, Any] = None) -> str:
        """Format command template with captured groups and context"""
        if match.groups():
            # Handle special formatting for different command types
            if template.count('{}') == len(match.groups()):
                return template.format(*match.groups())
            elif template.count('{}') == len(match.groups()) + 1:
                # Handle cases where we need context (like directory for find commands)
                groups = list(match.groups())
                if context and 'current_directory' in context:
                    groups.append(f' "{context["current_directory"]}"')
                else:
                    groups.append('')
                return template.format(*groups)
        
        return template
    
    def _try_contextual_patterns(self, text: str, context: Dict[str, Any]) -> Optional[Tuple[str, float]]:
        """Try context-aware pattern matching"""
        last_command_type = context.get('last_command_type')
        
        if last_command_type in self.contextual_patterns:
            patterns = self.contextual_patterns[last_command_type]
            for pattern, command_template in patterns.items():
                if re.search(pattern, text, re.IGNORECASE):
                    # Format with context
                    command = command_template.format(
                        last_file=context.get('last_file', ''),
                        current_directory=context.get('current_directory', '')
                    )
                    return command, 0.9  # High confidence for contextual matches
        
        return None
    
    def _try_ai_parsing(self, text: str, context: Dict[str, Any] = None) -> Optional[Tuple[str, float, List[str], Dict[str, Any]]]:
        """
        Placeholder for AI model integration
        Future implementation could integrate with GPT, Claude, or local models
        """
        # This would integrate with an AI model API
        # For now, return None to fall back to pattern matching
        return None
    
    def _is_direct_command(self, text: str) -> bool:
        """Enhanced direct command detection"""
        windows_commands = [
            'dir', 'cd', 'cls', 'echo', 'type', 'copy', 'move', 'del', 'mkdir', 
            'rmdir', 'ping', 'ipconfig', 'netstat', 'tasklist', 'taskkill',
            'help', 'exit', 'set', 'find', 'findstr', 'tree', 'attrib'
        ]
        
        # Check if starts with any command
        return any(text.startswith(cmd + ' ') or text == cmd for cmd in windows_commands)
    
    def _is_safe_command(self, command: str) -> bool:
        """Enhanced safety checking"""
        return not any(re.search(pattern, command, re.IGNORECASE) for pattern in self.danger_patterns)
    
    def _generate_enhanced_suggestions(self, text: str, context: Dict[str, Any] = None) -> List[str]:
        """Generate contextual and enhanced suggestions"""
        suggestions = []
        
        # Keyword-based suggestions
        keyword_suggestions = {
            'file': [
                'create a file named example.txt',
                'delete the file old.txt', 
                'show the content of README.md'
            ],
            'folder': [
                'create a folder named MyFolder',
                'go to the Documents folder',
                'list files in the current folder'
            ],
            'list': [
                'list all files',
                'list running processes',
                'show network connections'
            ],
            'copy': [
                'copy file.txt to backup.txt',
                'copy Documents folder to Desktop'
            ],
            'show': [
                'show current directory',
                'show date and time',
                'show file content'
            ]
        }
        
        # Find relevant suggestions
        for keyword, suggestion_list in keyword_suggestions.items():
            if keyword in text:
                suggestions.extend([f"💡 Try: '{s}'" for s in suggestion_list[:2]])
                break
        
        # Context-based suggestions
        if context:
            if context.get('last_command_type') == 'cd':
                suggestions.append("💡 Try: 'list files' or 'show contents'")
            elif context.get('last_command_type') == 'create':
                suggestions.append("💡 Try: 'edit it' or 'show it'")
        
        # Fuzzy matching suggestions (simplified)
        if not suggestions:
            common_commands = [
                'list all files', 'go to Documents', 'create file test.txt',
                'show current directory', 'copy file to backup'
            ]
            suggestions.extend([f"💡 Try: '{cmd}'" for cmd in common_commands[:2]])
        
        return suggestions[:3]
    
    def load_user_preferences(self) -> Dict[str, Any]:
        """Load user preferences from file"""
        prefs_file = Path("user_preferences.json")
        default_prefs = {
            'frequent_commands': [],
            'preferred_patterns': {},
            'safety_level': 'medium'
        }
        
        if prefs_file.exists():
            try:
                with open(prefs_file, 'r') as f:
                    return {**default_prefs, **json.load(f)}
            except:
                pass
        
        return default_prefs
    
    def _update_user_preferences(self, input_text: str, command: str):
        """Update user preferences based on usage"""
        if input_text not in self.user_preferences['frequent_commands']:
            self.user_preferences['frequent_commands'].append(input_text)
            
        # Keep only last 50 frequent commands
        if len(self.user_preferences['frequent_commands']) > 50:
            self.user_preferences['frequent_commands'] = \
                self.user_preferences['frequent_commands'][-50:]
        
        # Save preferences
        try:
            with open("user_preferences.json", 'w') as f:
                json.dump(self.user_preferences, f, indent=2)
        except:
            pass
    
    def get_command_suggestions(self, partial_input: str) -> List[str]:
        """Get real-time command suggestions as user types"""
        suggestions = []
        
        # Check frequent commands
        for cmd in self.user_preferences.get('frequent_commands', []):
            if partial_input.lower() in cmd.lower():
                suggestions.append(cmd)
        
        # Add common completions
        common_completions = {
            'create': ['create a file named', 'create a folder named'],
            'delete': ['delete the file', 'delete the folder'],
            'go': ['go to Documents', 'go to Desktop', 'go back'],
            'list': ['list all files', 'list running processes'],
            'show': ['show current directory', 'show file content']
        }
        
        for prefix, completions in common_completions.items():
            if partial_input.lower().startswith(prefix):
                suggestions.extend(completions)
        
        return suggestions[:5]  # Limit to 5 suggestions
