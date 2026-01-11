from langchain.tools import tool
import os
import subprocess
from langchain_core.tools import tool

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
    """Reads content from file."""
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
        with open(file=filepath, mode=mode) as f:
            f.write(content + "\n")
            return f"{content} has been written successfully"

    except Exception as e:
        return f"Error faced: {e}"

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
def install_package(package_name: str, dev_dependency: bool = False) -> str:
    """
    Installs an npm package. 
    Args:
        package_name: The name of the package (e.g., 'axios' or 'framer-motion').
        dev_dependency: Set to True if it is a dev dependency (e.g., --save-dev).
    """
    try:
        # Construct the command
        command = ["npm", "install"]
        
        if dev_dependency:
            command.append("-D")
            
        # Split package names if multiple are provided (e.g. "react-router-dom axios")
        packages = package_name.split()
        command.extend(packages)
        
        print(f"📦 Installing: {' '.join(packages)}... Please wait ⏱️⏱️")
        
        # Run the command
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        return f"Successfully installed: {package_name}\nOutput: {result.stdout}"

    except subprocess.CalledProcessError as e:
        return f"Failed to install {package_name}.\nError: {e.stderr}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
tools = [list_contents, get_curr_dir, create_dir, change_dir, read_file, write_to_file, remove_file, remove_dir, install_package]