import pickle
from pathlib import Path
import os

APPDATA_PATH = Path(os.getenv('LOCALAPPDATA') + '/VirtualRocks/recents.pkl').as_posix()

def add(path):
    """
    Method to add elements to the recents stack. If the passed path to a pkl file isn't already in
    recents, then it's appended to the stack. If the path is already in the stack, it's removed and
    reappended to move it to the top of the stack.

    Args:
        path (pathlib.Path): the path to the pkl project file to add to recents.
    """
    stack = get()
    if path not in stack:
        stack.append(path)
    else:
        stack.remove(path)
        stack.append(path)
    _dump_pkl(stack)

def remove(path):
    """
    Method to remove elements from the recents stack. The passed path gets removed from the recent
    stack, assuming it was in the stack originally.

    Args:
        path (pathlib.Path): the path to the pkl project file to remove from recents.
    """
    stack = get()
    if path in stack:
        stack.remove(path)
    _dump_pkl(stack)

def get():
    """
    Method that gets the recents stack out of the pkl and returns it. Used by `add` and
    `remove` to get the current value of the stack. 
    
    Called in :ref:`AppWindow.py <appwindow>` to initialize the menu.

    Returns:
        stack: the stack saved to the pkl file.
    """
    init_pkl()
    with open(APPDATA_PATH, 'rb') as file:
        stack = pickle.load(file)
    return stack

def init_pkl():
    """
    Method to initialize the recents pkl file if it doesn't already exist in the user's AppData.
    Called in `_load_pkl` to make sure the pkl file exists before use.
    """
    if not os.path.isdir(os.path.join(os.getenv('LOCALAPPDATA'), "VirtualRocks")):
        os.mkdir(os.path.join(os.getenv('LOCALAPPDATA'), "VirtualRocks"))
    if not os.path.isfile(APPDATA_PATH):
        with open(APPDATA_PATH, 'wb') as file:
            pickle.dump([], file)

def _dump_pkl(stack):
    """
    Helper method to save any changes made to the stack to the pkl file. Only the 4 most recent pkl
    files (the last 4 elements in the stack) are retained.
    """
    stack = stack[-4:]
    with open(APPDATA_PATH, 'wb') as file:
        pickle.dump(stack, file)