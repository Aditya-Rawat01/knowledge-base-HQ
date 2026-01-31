from langchain.tools import tool
import os
import subprocess
from langchain_core.tools import tool

@tool
def search_codebase(query: str, path: str = ".") -> str:
    """
    Searches for a string pattern inside all files in the directory (recursive).
    Useful for finding where a specific function or variable is defined.
    Ignores .git and node_modules.
    """
    try:
        # We use grep (Linux/Mac) or simple python walk for cross-platform compatibility
        matches = []
        for root, dirs, files in os.walk(path):
            # Prune directories to save time
            if 'node_modules' in dirs: dirs.remove('node_modules')
            if '.git' in dirs: dirs.remove('.git')
            if '__pycache__' in dirs: dirs.remove('__pycache__')
            
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', errors='ignore') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            if query in line:
                                matches.append(f"{file_path}:{i+1}: {line.strip()}")
                                if len(matches) > 20: # Limit results
                                    return "\n".join(matches) + "\n... (more results truncated)"
                except:
                    continue
        
        return "\n".join(matches) if matches else "No matches found."
    except Exception as e:
        return f"Error searching: {e}"

@tool
def list_contents(path: str)->str:
    """Lists files and folders for given path folder."""
    try:
        if not path:
            path = os.curdir
        result = os.listdir(path)
        print(f"{result} are the list of the files present in {path} ")
        return f"{result} are the list of the files present here."
    except Exception as e:
        return f"Error faced: {e}"

@tool
def get_curr_dir()->str:
    """Lists files and folders in current directory."""
    try:
        result = os.listdir()
        return f"{result} are the list of the files present in current directory"
    except Exception as e:
        return f"Error faced: {e}"

@tool
def create_dir(path:str)->str:
    """Creates directory recursively. Requires 'path'."""
    try:
        os.makedirs(path, exist_ok=True)
        return f"{path} directory has been created successfully"
    except Exception as e:
        return f"Error faced: {e}"

@tool
def change_dir(path:str)->str:
    """Changes current directory."""
    try:
        os.chdir(path)
        return f"current working directory is {os.getcwd()}"
    except Exception as e:
        return f"Error faced: {e}"
    
@tool
def read_file(filepath:str)->str:
    """Reads content from file. Reads max 200 lines to prevent overload."""
    try:
        with open(filepath, "r") as f:
            content = f.read()
            return content
    except Exception as e:
        return f"Error faced: {e}"

@tool  
def write_to_file(filepath:str, content:str , mode='w')->str:
    """Writes content to file. Mode: 'w' for write, 'a' for append."""
    try:
        if not os.path.exists(filepath):
            return f"Error: File {filepath} does not exist."
            
        with open(filepath, "r", encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
            # FAULT TOLERANCE: Limit output
            MAX_LINES = 200
            if len(lines) > MAX_LINES:
                content = "".join(lines[:MAX_LINES])
                return f"{content}\n\n... [File truncated at line {MAX_LINES} out of {len(lines)}. Use search_codebase to find specific parts.]"
            
            return "".join(lines)
    except Exception as e:
        return f"Error reading file: {e}"

@tool
def remove_file(filepath:str)->str:
    """Removes file from the given path folder. Must use carefully!"""
    try:
        os.remove(filepath)
        return f"{filepath} has been deleted successfully"
    except Exception as e:
        return f"Error faced: {e}"

@tool
def remove_dir(filepath:str)->str:
    """Removes sub folder from the given path folder. Must use carefully!"""
    try:
        os.rmdir(filepath)
        return f"{filepath} has been deleted successfully"
    except Exception as e:
        return f"Error faced: {e}"


@tool
def run_terminal_command(command: str) -> str:
    """
    Executes a shell command. Use this for installing packages, running tests, or file operations not covered by other tools.
    Examples: 'pip install pandas', 'npm install axios', 'ls -la', 'python main.py'.
    """
    # FAULT TOLERANCE: blacklist dangerous commands
    blacklist = ["rm -rf /", "rm -rf ~", "sudo", "format"]
    if any(b in command for b in blacklist):
        return "Error: Command blocked for safety reasons."

    try:
        print(f"💻 Running: {command}")
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd=os.getcwd() # Ensure it runs in the current context
        )
        
        # Capture standard out and standard error
        output = result.stdout
        if result.stderr:
            output += f"\n[STDERR]: {result.stderr}"
            
        return output if output.strip() else "Command executed with no output."
    except Exception as e:
        return f"Failed to execute command: {e}"
tools = [list_contents, get_curr_dir, create_dir, change_dir, read_file, write_to_file, remove_file, remove_dir, run_terminal_command]