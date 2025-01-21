import subprocess
import sys
import os

# Correct path to the virtual environment's Python interpreter
venv_python = r"D:\Git\Python\SPL\project\.test\Scripts\python.exe"

# Check if python.exe exists at the given path
if not os.path.exists(venv_python):
    print(f"Error: {venv_python} not found. Please check the venv path.")
    sys.exit(1)

# Start the Django server
try:
    subprocess.run([venv_python, "manage.py", "runserver", "0.0.0.0:8000"])
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
