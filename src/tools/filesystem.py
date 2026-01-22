import os

# Set the root directory Dustin is allowed to see (e.g., your Projects folder)
# You can change this to specific paths like your OmniSolve or Tarot Game folders.
ALLOWED_ROOT = "C:/Users/Michael/Projects" 

def list_directory(path="."):
    """Lists files in a given directory relative to the root."""
    target_path = os.path.join(ALLOWED_ROOT, path)
    
    if not os.path.exists(target_path):
        return f"Error: Path '{path}' does not exist."
    
    try:
        items = os.listdir(target_path)
        return f"Contents of {path}: {', '.join(items)}"
    except Exception as e:
        return f"Error reading directory: {str(e)}"

def read_file(filename):
    """Reads the content of a specific file."""
    target_path = os.path.join(ALLOWED_ROOT, filename)
    
    if not os.path.exists(target_path):
        return "Error: File not found."
    
    try:
        with open(target_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"
    
def create_file(filename, content):
        """Creates a new file with the given content."""
        target_path = os.path.join(ALLOWED_ROOT, filename)
        
        # Safety Check: Don't overwrite unless explicitly handled (or just return error)
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