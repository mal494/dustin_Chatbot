import os
import subprocess  # <--- Essential for running scripts

# Set this to "." to allow creating files in the main folder
ALLOWED_ROOT = "."

def list_directory(path="."):
    """Lists files in the given directory."""
    target_path = os.path.join(ALLOWED_ROOT, path)
    if not os.path.exists(target_path):
        return "Error: Directory not found."
    
    try:
        items = os.listdir(target_path)
        return f"Contents of {path}: {', '.join(items)}"
    except Exception as e:
        return f"Error: {str(e)}"

def read_file(filename):
    """Reads a file and returns its content."""
    target_path = os.path.join(ALLOWED_ROOT, filename)
    if not os.path.exists(target_path):
        return "Error: File not found."
    
    try:
        with open(target_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def create_file(filename, content):
    """Creates a new file. Fails if file already exists."""
    target_path = os.path.join(ALLOWED_ROOT, filename)
    if os.path.exists(target_path):
        return f"Error: File '{filename}' already exists. Use 'overwrite_file' if you are sure."
    
    try:
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Success: Created '{filename}'."
    except Exception as e:
        return f"Error writing file: {str(e)}"

def overwrite_file(filename, content):
    """Overwrites an existing file. USE WITH CAUTION."""
    target_path = os.path.join(ALLOWED_ROOT, filename)
    try:
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Success: Updated '{filename}'."
    except Exception as e:
        return f"Error updating file: {str(e)}"

def run_script(filename):
    """Executes a python script and returns the output."""
    target_path = os.path.join(ALLOWED_ROOT, filename)
    
    if not os.path.exists(target_path):
        return f"Error: File '{filename}' not found."
    
    try:
        # We set a timeout of 10 seconds to prevent infinite loops
        result = subprocess.run(
            ["python", target_path], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        # Return success or error messages
        if result.returncode == 0:
            return f"✅ Execution Success. Output:\n{result.stdout}"
        else:
            return f"❌ Execution Error. Traceback:\n{result.stderr}"
            
    except subprocess.TimeoutExpired:
        return "Error: Script timed out (ran longer than 10 seconds)."
    except Exception as e:
        return f"System Error: {str(e)}"