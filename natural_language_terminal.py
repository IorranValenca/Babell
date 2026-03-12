import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from natural_language_parser import NaturalLanguageParser
from command_executor import CommandExecutor

class NaturalLanguageTerminal:
    """
    Babell - A modern terminal interface that understands natural language commands
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Babell")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1e1e1e')
        
        # Set window icon
        try:
            from icon_utils import set_window_icon
            set_window_icon(self.root, "BABELL.png")
        except ImportError:
            # Fallback: try basic icon loading
            try:
                self.root.iconbitmap('BABELL.png')
            except:
                pass  # Use default icon if loading fails
        
        # Initialize components
        self.parser = NaturalLanguageParser()
        self.executor = CommandExecutor()
        self.command_history = []
        self.history_index = -1
        
        # Load settings
        self.settings_file = Path("terminal_settings.json")
        self.settings = self.load_settings()
        
        # Setup GUI
        self.setup_styles()
        self.create_widgets()
        self.setup_bindings()
        
        # Welcome message
        self.display_welcome_message()
    
    def setup_styles(self):
        """Configure modern dark theme styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'accent': '#0078d4',
            'success': '#16c60c',
            'warning': '#ffb900',
            'error': '#d13438',
            'input_bg': '#2d2d30',
            'output_bg': '#0c0c0c'
        }
        
        # Configure fonts
        self.fonts = {
            'mono': font.Font(family="Consolas", size=10),
            'mono_bold': font.Font(family="Consolas", size=10, weight="bold"),
            'ui': font.Font(family="Segoe UI", size=9)
        }
    
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self.create_header(main_frame)
        
        # Output area
        self.create_output_area(main_frame)
        
        # Input area
        self.create_input_area(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Create header with title and controls"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="🤖 Babell",
            font=self.fonts['mono_bold'],
            bg=self.colors['bg'],
            fg=self.colors['accent']
        )
        title_label.pack(side=tk.LEFT)
        
        # Controls
        controls_frame = ttk.Frame(header_frame)
        controls_frame.pack(side=tk.RIGHT)
        
        ttk.Button(
            controls_frame,
            text="Clear",
            command=self.clear_output
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            controls_frame,
            text="Help",
            command=self.show_help
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            controls_frame,
            text="Settings",
            command=self.show_settings
        ).pack(side=tk.LEFT)
    
    def create_output_area(self, parent):
        """Create scrollable output area"""
        output_frame = ttk.LabelFrame(parent, text="Output", padding=5)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            font=self.fonts['mono'],
            bg=self.colors['output_bg'],
            fg=self.colors['fg'],
            insertbackground=self.colors['accent'],
            selectbackground=self.colors['accent'],
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for colored output
        self.output_text.tag_configure('success', foreground=self.colors['success'])
        self.output_text.tag_configure('error', foreground=self.colors['error'])
        self.output_text.tag_configure('warning', foreground=self.colors['warning'])
        self.output_text.tag_configure('info', foreground=self.colors['accent'])
        self.output_text.tag_configure('prompt', foreground=self.colors['accent'], font=self.fonts['mono_bold'])
    
    def create_input_area(self, parent):
        """Create input area with natural language entry"""
        input_frame = ttk.LabelFrame(parent, text="Natural Language Command", padding=5)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Input field
        self.input_entry = tk.Entry(
            input_frame,
            font=self.fonts['mono'],
            bg=self.colors['input_bg'],
            fg=self.colors['fg'],
            insertbackground=self.colors['accent'],
            selectbackground=self.colors['accent'],
            relief=tk.FLAT,
            bd=5
        )
        self.input_entry.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=(0, 10))
        
        # Execute button
        self.execute_button = ttk.Button(
            input_frame,
            text="Execute",
            command=self.execute_command
        )
        self.execute_button.pack(side=tk.RIGHT)
        
        # Suggestions area
        self.suggestions_frame = ttk.Frame(input_frame)
        self.suggestions_frame.pack(fill=tk.X, pady=(5, 0))
    
    def create_status_bar(self, parent):
        """Create status bar with current directory and other info"""
        self.status_bar = ttk.Frame(parent)
        self.status_bar.pack(fill=tk.X)
        
        # Current directory
        self.dir_label = tk.Label(
            self.status_bar,
            text=f"📁 {self.executor.get_current_directory()}",
            font=self.fonts['ui'],
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            anchor=tk.W
        )
        self.dir_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Command count
        self.command_count_label = tk.Label(
            self.status_bar,
            text="Commands: 0",
            font=self.fonts['ui'],
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.command_count_label.pack(side=tk.RIGHT, padx=(10, 0))
    
    def setup_bindings(self):
        """Setup keyboard bindings"""
        self.input_entry.bind('<Return>', lambda e: self.execute_command())
        self.input_entry.bind('<Up>', self.previous_command)
        self.input_entry.bind('<Down>', self.next_command)
        self.input_entry.bind('<Control-c>', self.interrupt_command)
        self.input_entry.bind('<KeyRelease>', self.on_input_change)
        
        # Focus on input field
        self.input_entry.focus_set()
    
    def display_welcome_message(self):
        """Display welcome message with instructions"""
        welcome_text = f"""
🤖 Welcome to Babell!

Current Directory: {self.executor.get_current_directory()}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Examples of natural language commands you can try:

📁 File Operations:
• "list all files"
• "create a new file called test.txt"
• "go to Documents folder"

🔧 Programming & Development:
• "git status"
• "npm install express"
• "run python file script.py"
• "create react app myproject"
• "docker build myapp"
• "pip install requests"

💻 Code Creation:
• "create html file index"
• "create python file main"
• "open in vscode app.js"

You can also use regular terminal commands directly.
Type 'help' for more information or use the Help button.

─────────────────────────────────────────────────────────
"""
        self.append_output(welcome_text, 'info')
    
    def append_output(self, text: str, tag: str = None):
        """Append text to output area with optional formatting"""
        self.output_text.config(state=tk.NORMAL)
        if tag:
            self.output_text.insert(tk.END, text, tag)
        else:
            self.output_text.insert(tk.END, text)
        self.output_text.config(state=tk.DISABLED)
        self.output_text.see(tk.END)
    
    def execute_command(self):
        """Execute the natural language command"""
        user_input = self.input_entry.get().strip()
        if not user_input:
            return
        
        # Add to history
        self.command_history.append(user_input)
        self.history_index = len(self.command_history)
        
        # Display user input
        prompt = f"\\n💬 You: {user_input}\\n"
        self.append_output(prompt, 'prompt')
        
        # Parse natural language
        current_dir = self.executor.get_current_directory()
        command, confidence, suggestions = self.parser.parse_command(user_input, current_dir)
        
        if command:
            # Show parsed command if it's different from input
            if command.lower() != user_input.lower():
                self.append_output(f"🔄 Interpreted as: {command}\\n", 'info')
            
            # Show confidence level
            if confidence < 1.0:
                confidence_text = f"🎯 Confidence: {confidence:.0%}\\n"
                self.append_output(confidence_text, 'warning')
            
            # Execute command
            result = self.executor.execute_command(command)
            self.display_command_result(result)
            
        else:
            self.append_output("❌ Could not understand the command.\\n", 'error')
        
        # Show suggestions
        if suggestions:
            self.append_output("\\n💡 Suggestions:\\n", 'info')
            for suggestion in suggestions:
                self.append_output(f"   {suggestion}\\n", 'warning')
        
        # Update status
        self.update_status()
        
        # Clear input
        self.input_entry.delete(0, tk.END)
    
    def display_command_result(self, result: dict):
        """Display the result of command execution"""
        if result['success']:
            if result['output']:
                self.append_output(f"✅ Output:\\n{result['output']}\\n", 'success')
            else:
                self.append_output("✅ Command executed successfully.\\n", 'success')
        else:
            error_msg = result['error'] if result['error'] else 'Command failed'
            self.append_output(f"❌ Error: {error_msg}\\n", 'error')
    
    def on_input_change(self, event):
        """Handle input changes to show live suggestions"""
        # This could be enhanced to show live suggestions as user types
        pass
    
    def previous_command(self, event):
        """Navigate to previous command in history"""
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.command_history[self.history_index])
    
    def next_command(self, event):
        """Navigate to next command in history"""
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.command_history[self.history_index])
        elif self.history_index >= len(self.command_history) - 1:
            self.history_index = len(self.command_history)
            self.input_entry.delete(0, tk.END)
    
    def interrupt_command(self, event):
        """Interrupt currently running command"""
        if self.executor.interrupt_command():
            self.append_output("\\n⏹️ Command interrupted.\\n", 'warning')
    
    def clear_output(self):
        """Clear the output area"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.display_welcome_message()
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
Babell Help

SUPPORTED COMMANDS:

📁 File Operations: create, delete, copy, move, rename files/folders
📂 Navigation: go to directory, go back, go home  
👀 Viewing: list files, show content, find files
⚙️ System: show date/time, clear screen, show processes
🌐 Network: ping, show connections, show IP config

🔧 Programming & Development:
• Git: "git status", "git add all", "git commit with message 'fix'"
• NPM: "npm install express", "npm run build", "npm test"
• Python: "run python file script.py", "pip install requests"
• Docker: "docker build myapp", "docker run container"
• Code Creation: "create html file index", "create python file main"

EXAMPLES:
• "create a file called notes.txt"
• "git status"  
• "npm install react"
• "run python file main.py"
• "create react app myproject"
• "docker build myapp"
• "open in vscode app.js"

KEYBOARD SHORTCUTS:
• Enter: Execute command
• Up/Down: Navigate command history
• Ctrl+C: Interrupt running command

You can also type regular terminal commands directly!
        """
        messagebox.showinfo("Help", help_text)
    
    def show_settings(self):
        """Show settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.configure(bg=self.colors['bg'])
        
        # Add settings controls here
        tk.Label(
            settings_window,
            text="Settings (Future Enhancement)",
            font=self.fonts['ui'],
            bg=self.colors['bg'],
            fg=self.colors['fg']
        ).pack(pady=20)
    
    def update_status(self):
        """Update status bar information"""
        # Update directory
        current_dir = self.executor.get_current_directory()
        self.dir_label.config(text=f"📁 {current_dir}")
        
        # Update command count
        count = len(self.command_history)
        self.command_count_label.config(text=f"Commands: {count}")
    
    def load_settings(self) -> dict:
        """Load settings from file"""
        default_settings = {
            'theme': 'dark',
            'font_size': 10,
            'auto_suggestions': True,
            'command_timeout': 30
        }
        
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    return {**default_settings, **json.load(f)}
            except:
                pass
        
        return default_settings
    
    def save_settings(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Failed to save settings: {e}")
    
    def run(self):
        """Start the terminal application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass
        finally:
            self.save_settings()

if __name__ == "__main__":
    terminal = NaturalLanguageTerminal()
    terminal.run()
