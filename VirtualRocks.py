import os
import subprocess
import sys

# This file is only for the compiler and installer 
PYTHONPATH = os.environ['PROGRAMFILES'] + "/python311/python"

pklfile = ""
try:
    pklfile = sys.argv[1]
    print(pklfile)
except:
    pass

subprocess.Popen([PYTHONPATH, 'main.py'])
