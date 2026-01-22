import webview
import subprocess
import sys
import time
import threading
import socket

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def run_streamlit():
    """Starts Streamlit silently in the background."""
    # We use sys.executable to ensure we use the same Python environment
    # --server.headless=true prevents Streamlit from trying to open a browser tab automatically
    cmd = [sys.executable, "-m", "streamlit", "run", "main.py", "--server.headless=true"]
    subprocess.run(cmd)

if __name__ == '__main__':
    # 1. Start Streamlit in a separate thread so it doesn't block the UI
    if not is_port_in_use(8501):
        t = threading.Thread(target=run_streamlit)
        t.daemon = True # Ensures this thread dies when the main app closes
        t.start()
        print("Starting Dustin AI Engine...")
        time.sleep(3) # Give Streamlit a moment to warm up
    else:
        print("Dustin is already running in the background.")

    # 2. Create the Native Window
    # width/height sets the initial size. resizable=True allows you to stretch it.
    webview.create_window(
        "Dustin AI", 
        "http://localhost:8501", 
        width=1000, 
        height=800,
        resizable=True
    )

    # 3. Start the App
    webview.start()