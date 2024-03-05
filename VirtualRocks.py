import os
import subprocess
import sys

# This file is only for the compiler and installer 
# Run: pyinstaller --onefile VirtualRocks.py

PYTHONPATH = os.getenv('LOCALAPPDATA') + "\\Programs\\Python\\Python311\\python.exe"
MAINPATH = os.getenv('LOCALAPPDATA') + "\\Programs\\VirtualRocks\\main.py"

pklfile = ""
try:
    pklfile = sys.argv[1]
except:
    pass

cwd = os.getenv('LOCALAPPDATA') + "\\Programs\\VirtualRocks"
p = subprocess.Popen([PYTHONPATH, MAINPATH, pklfile], cwd=str(cwd))
p.wait()

# Installer script stuff...
"""
[Run]
Filename: "{tmp}\python-3.11.5-amd64.exe"; Parameters: "/quiet InstallAllUsers=0 PrependPath=1"; StatusMsg: "Installing Python..."; Flags: waituntilterminated;
#define PipPath "{localappdata}\Programs\Python\Python311\Scripts\pip.exe"
Filename: "{#PipPath}"; Parameters: "install ttkbootstrap"; Flags: runhidden; StatusMsg: "Installing ttkbootstrap..."
Filename: "{#PipPath}"; Parameters: "install pymeshlab"; Flags: runhidden; StatusMsg: "Installing pymeshlab..."
Filename: "{#PipPath}"; Parameters: "install plyfile"; Flags: runhidden; StatusMsg: "Installing plyfile..."
Filename: "{#PipPath}"; Parameters: "install open3d"; Flags: runhidden; StatusMsg: "Installing open3d..."
Filename: "{#PipPath}"; Parameters: "install show_in_file_manager"; Flags: runhidden; StatusMsg: "Installing showifm..."
Filename: "{#PipPath}"; Parameters: "install matplotlib"; Flags: runhidden; StatusMsg: "Installing matplotlib..."
"""