import subprocess
import threading
import os
import sys
from typing import Callable, Optional
from pathlib import Path

class CommandExecutor:
    """
    Safely executes system commands with proper error handling
    """
    
    def __init__(self, output_callback: Callable[[str, str], None] = None):
        self.output_callback = output_callback
        self.current_directory = Path.cwd()
        self.running_process = None
        
    def execute_command(self, command: str, timeout: int = 30) -> dict:
        """
        Execute a system command and return results
        Returns: dict with 'success', 'output', 'error', 'return_code'
        """
        try:
            # Handle cd command specially to maintain directory state
            if command.strip().startswith('cd'):
                return self._handle_cd_command(command)
            
            # Execute command in current directory
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='ignore',
                cwd=str(self.current_directory),
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            
            self.running_process = process
            
            try:
                stdout, stderr = process.communicate(timeout=timeout)
                return_code = process.returncode
                
                result = {
                    'success': return_code == 0,
                    'output': stdout.strip() if stdout else '',
                    'error': stderr.strip() if stderr else '',
                    'return_code': return_code,
                    'command': command
                }
                
                # Call output callback if provided
                if self.output_callback:
                    self.output_callback(stdout, stderr)
                
                return result
                
            except subprocess.TimeoutExpired:
                process.kill()
                return {
                    'success': False,
                    'output': '',
                    'error': f'Command timed out after {timeout} seconds',
                    'return_code': -1,
                    'command': command
                }
                
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': f'Failed to execute command: {str(e)}',
                'return_code': -1,
                'command': command
            }
        finally:
            self.running_process = None
    
    def execute_async(self, command: str, callback: Callable[[dict], None]):
        """Execute command asynchronously"""
        def run():
            result = self.execute_command(command)
            callback(result)
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
    
    def _handle_cd_command(self, command: str) -> dict:
        """Handle directory changes to maintain state"""
        parts = command.strip().split(None, 1)
        
        if len(parts) == 1:  # Just 'cd' - show current directory
            return {
                'success': True,
                'output': str(self.current_directory),
                'error': '',
                'return_code': 0,
                'command': command
            }
        
        target_path = parts[1].strip('"').strip("'")
        
        # Handle special cases
        if target_path == '..':
            new_path = self.current_directory.parent
        elif target_path.startswith('%') and target_path.endswith('%'):
            # Handle environment variables
            env_var = target_path[1:-1]
            env_path = os.environ.get(env_var)
            if env_path:
                new_path = Path(env_path)
            else:
                return {
                    'success': False,
                    'output': '',
                    'error': f'Environment variable {env_var} not found',
                    'return_code': 1,
                    'command': command
                }
        else:
            # Handle absolute or relative paths
            if Path(target_path).is_absolute():
                new_path = Path(target_path)
            else:
                new_path = self.current_directory / target_path
        
        # Check if path exists and is a directory
        try:
            new_path = new_path.resolve()
            if new_path.exists() and new_path.is_dir():
                self.current_directory = new_path
                return {
                    'success': True,
                    'output': f'Changed directory to: {new_path}',
                    'error': '',
                    'return_code': 0,
                    'command': command
                }
            else:
                return {
                    'success': False,
                    'output': '',
                    'error': f'Directory not found: {new_path}',
                    'return_code': 1,
                    'command': command
                }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': f'Invalid path: {str(e)}',
                'return_code': 1,
                'command': command
            }
    
    def get_current_directory(self) -> str:
        """Get current working directory"""
        return str(self.current_directory)
    
    def interrupt_command(self):
        """Interrupt currently running command"""
        if self.running_process:
            try:
                self.running_process.terminate()
                return True
            except:
                return False
        return False
