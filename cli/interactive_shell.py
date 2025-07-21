import typer
import subprocess
import sys
import os
from typing import Dict, Any
from auth_cli import app as auth_app
from projects_cli import app as projects_app
from hr_cli import app as hr_app
from documents_cli import app as documents_app
from materials_cli import app as materials_app
from manufacturing_cli import app as manufacturing_app
from logistics_cli import app as logistics_app
from finance_cli import app as finance_app
from products_cli import app as products_app
from vehicles_cli import app as vehicles_app
from referentiels_cli import app as referentiels_app
from common_cli import app as common_app
from auth_manager import load_token

class InteractiveCLI:
    def __init__(self):
        self.modules = {
            "auth": auth_app,
            "projects": projects_app,
            "hr": hr_app,
            "documents": documents_app,
            "materials": materials_app,
            "manufacturing": manufacturing_app,
            "logistics": logistics_app,
            "finance": finance_app,
            "products": products_app,
            "vehicles": vehicles_app,
            "referentiels": referentiels_app,
            "common": common_app,
        }
        self.current_module = None
        
    def print_welcome(self):
        print("\n🚀 Welcome to PMS Efficience Interactive CLI")
        print("=" * 50)
        token = load_token()
        if token:
            print("✅ You are logged in")
        else:
            print("❌ Not logged in - use 'auth login' to authenticate")
        print("\nAvailable modules:")
        for module_name in self.modules.keys():
            print(f"  - {module_name}")
        print("\nCommands:")
        print("  help          - Show this help")
        print("  modules       - List available modules")
        print("  <module>      - Enter a module (e.g., 'auth', 'projects')")
        print("  exit/quit     - Exit the CLI")
        print()

    def print_module_help(self, module_name):
        print(f"\n📁 {module_name.upper()} Module")
        print("=" * 30)
        
        # Get commands from the typer app
        try:
            app = self.modules[module_name]
            commands_found = False
            
            # Check various ways Typer might store commands
            if hasattr(app, 'commands'):
                commands = app.commands
                print("Available commands:")
                
                # Handle if commands is a dict
                if isinstance(commands, dict):
                    for cmd_name, cmd in commands.items():
                        doc = getattr(cmd.callback, '__doc__', None) or "No description"
                        doc = doc.strip().split('\n')[0] if doc else "No description"
                        print(f"  {cmd_name:<20} - {doc}")
                    commands_found = True
                    
                # Handle if commands is a list
                elif isinstance(commands, list):
                    for cmd in commands:
                        if hasattr(cmd, 'name') and hasattr(cmd, 'callback'):
                            cmd_name = cmd.name or getattr(cmd.callback, '__name__', 'unknown')
                            doc = getattr(cmd.callback, '__doc__', None) or "No description"
                            doc = doc.strip().split('\n')[0] if doc else "No description"
                            print(f"  {cmd_name:<20} - {doc}")
                            commands_found = True
                        elif hasattr(cmd, 'callback'):
                            cmd_name = getattr(cmd.callback, '__name__', 'unknown')
                            doc = getattr(cmd.callback, '__doc__', None) or "No description"
                            doc = doc.strip().split('\n')[0] if doc else "No description"
                            print(f"  {cmd_name:<20} - {doc}")
                            commands_found = True
                            
            # Try registered_commands if commands didn't work
            if not commands_found and hasattr(app, 'registered_commands'):
                registered = app.registered_commands
                if isinstance(registered, dict):
                    print("Available commands:")
                    for cmd_name, cmd in registered.items():
                        doc = getattr(cmd.callback, '__doc__', None) or "No description"
                        doc = doc.strip().split('\n')[0] if doc else "No description"
                        print(f"  {cmd_name:<20} - {doc}")
                    commands_found = True
                    
            # Fallback: show predefined commands for each module
            if not commands_found:
                common_commands = {
                    'auth': ['login', 'logout', 'register'],
                    'projects': ['list', 'create', 'get'],
                    'hr': ['list-employees', 'create-employee', 'get-employee', 'update-employee', 'delete-employee'],
                    'documents': ['upload', 'get-metadata', 'delete'],
                    'materials': ['list', 'create', 'get', 'update'],
                    'manufacturing': ['list-bom', 'create-bom', 'list-orders', 'create-order'],
                    'logistics': ['list-deliveries', 'create-delivery', 'list-supply-requests'],
                    'finance': ['list-accounts', 'create-account', 'list-ledger-lines', 'trial-balance'],
                    'products': ['list-products', 'create-product', 'list-stocks', 'create-stock-move'],
                    'vehicles': ['list-vehicles', 'create-vehicle', 'add-km-log', 'assign-driver'],
                    'referentiels': ['list-devises', 'create-devise', 'list-expense-categories'],
                    'common': ['health']
                }
                
                if module_name in common_commands:
                    print("Typical commands:")
                    for cmd in common_commands[module_name]:
                        print(f"  {cmd:<20} - {cmd.replace('-', ' ').title()}")
                else:
                    print("Commands not auto-detected.")
                    
        except Exception as e:
            # Always fall back to predefined commands if there's any error
            common_commands = {
                'auth': ['login', 'logout', 'register'],
                'projects': ['list', 'create', 'get'],
                'hr': ['list-employees', 'create-employee', 'get-employee', 'update-employee', 'delete-employee'],
                'documents': ['upload', 'get-metadata', 'delete'],
                'materials': ['list', 'create', 'get', 'update'],
                'manufacturing': ['list-bom', 'create-bom', 'list-orders', 'create-order'],
                'logistics': ['list-deliveries', 'create-delivery', 'list-supply-requests'],
                'finance': ['list-accounts', 'create-account', 'list-ledger-lines', 'trial-balance'],
                'products': ['list-products', 'create-product', 'list-stocks', 'create-stock-move'],
                'vehicles': ['list-vehicles', 'create-vehicle', 'add-km-log', 'assign-driver'],
                'referentiels': ['list-devises', 'create-devise', 'list-expense-categories'],
                'common': ['health']
            }
            
            if module_name in common_commands:
                print("Typical commands:")
                for cmd in common_commands[module_name]:
                    print(f"  {cmd:<20} - {cmd.replace('-', ' ').title()}")
            else:
                print("Commands not available.")
        
        print("\nNavigation:")
        print("  back          - Return to main menu")
        print("  help          - Show this help")
        print("  exit/quit     - Exit the CLI")
        print()

    def execute_command(self, module_name, command_line):
        """Execute a command in the specified module using subprocess"""
        try:
            # Get the path to main.py
            main_py_path = os.path.join(os.path.dirname(__file__), 'main.py')
            
            # Build the command
            cmd_parts = [sys.executable, main_py_path, module_name] + command_line.split()
            
            print(f"⚡ Executing: {module_name} {command_line}")
            print("-" * 40)
            
            # Execute the command
            result = subprocess.run(cmd_parts, capture_output=False, text=True)
            
            print("-" * 40)
            if result.returncode == 0:
                print("✅ Command completed successfully")
            else:
                print(f"❌ Command failed with exit code {result.returncode}")
                
        except Exception as e:
            print(f"❌ Error executing command: {e}")
        
        print()  # Add spacing after command execution

    def run(self):
        self.print_welcome()
        
        while True:
            try:
                if self.current_module:
                    prompt = f"pms-cli ({self.current_module})> "
                else:
                    prompt = "pms-cli> "
                
                user_input = input(prompt).strip()
                
                if not user_input:
                    continue
                    
                parts = user_input.split()
                command = parts[0].lower()
                
                # Global commands (work anywhere)
                if command in ["exit", "quit"]:
                    print("👋 Goodbye!")
                    break
                    
                elif command == "help":
                    if self.current_module:
                        self.print_module_help(self.current_module)
                    else:
                        self.print_welcome()
                        
                elif command == "modules":
                    print("Available modules:")
                    for module_name in self.modules.keys():
                        print(f"  - {module_name}")
                    print()
                    
                elif command == "back":
                    if self.current_module:
                        print(f"← Exiting {self.current_module} module")
                        self.current_module = None
                    else:
                        print("Already at main menu")
                        
                # Module navigation
                elif command in self.modules:
                    if not self.current_module:
                        # Enter a module from main menu
                        self.current_module = command
                        print(f"→ Entered {command} module")
                        self.print_module_help(command)
                    else:
                        # Already in a module, suggest using back first
                        print(f"Already in '{self.current_module}' module.")
                        print(f"Use 'back' to return to main menu, then '{command}' to enter that module.")
                        
                # Command execution within modules
                elif self.current_module:
                    # Execute the command in the current module
                    self.execute_command(self.current_module, user_input)
                    
                # Unknown command
                else:
                    print(f"Unknown command: {command}")
                    if self.current_module:
                        print(f"Available commands in {self.current_module}: use 'help' to see them")
                        print(f"Or use 'back' to return to main menu")
                    else:
                        print("Type 'help' for available commands")
                        
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break

if __name__ == "__main__":
    cli = InteractiveCLI()
    cli.run() 