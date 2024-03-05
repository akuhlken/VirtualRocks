import os
import subprocess
import sys

# This file is only for the compiler and installer 
PYTHONPATH = os.environ['PROGRAMFILES'] + "/python311/python"

pklfile = ""
try:
    pklfile = sys.argv[1] # this actually works!
    print(pklfile)
except:
    pass

# need to figure out how to jump straight into open project with pkl file
subprocess.Popen([PYTHONPATH, 'main.py']) # needs to give full path to main because looking at location of pkl file
