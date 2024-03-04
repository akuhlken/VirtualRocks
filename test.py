import pickle
from pathlib import Path
import os

APPDATA_PATH = Path(os.getenv('LOCALAPPDATA') + '/VirtualRocks/recents.json').as_posix()

def add(path):
    with open(APPDATA_PATH, 'rb') as file:
        stack = pickle.load(file)
    if path not in stack:
        stack.append(path)
    else:
        stack.remove(path)
        stack.append(path)
    stack = stack[-4:]
    with open(APPDATA_PATH, 'wb') as file:
        pickle.dump(stack, file)

# for changing directory
def change(oldpath, newpath):
    with open(APPDATA_PATH, 'rb') as file:
        stack = pickle.load(file)
    stack.remove(oldpath)
    stack.append(newpath)
    stack = stack[-4:]
    with open(APPDATA_PATH, 'wb') as file:
        pickle.dump(stack, file)

def get():
    with open(APPDATA_PATH, 'rb') as file:
        stack = pickle.load(file)
    return stack