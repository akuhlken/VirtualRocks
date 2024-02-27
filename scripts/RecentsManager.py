from pathlib import Path
import json
import os

# TODO: add comments for things, probs wait until we understand what the auto-documentation wants.

class RecentsManager():

    RECENT_PATH = Path('gui/recents.json')

    def __init__(self):
        """
        Implements the recents functionality in the menu bar. The dictionary of recents stored by this class can be
        accessed with the ``get_recent()`` function, updated with the ``update_recent()`` function, and stored to an
        JSON file in the app files using ``save_recent()``. The dictionary of recents is initialized to the dictionary 
        stored in the JSON file when used in main and automatically saves on exit.
        """
        self.recentlist = self.get_recent() 

    def update_recent(self, pklpath):    
        """
        Updates the recent list maintained by the class. It stores the paths to up to 4 pickle files (the current
        and the 3 that came before it) in a dictionary and deletes the oldest 'recent' project file path when a 
        new file has been added. If a file path that already exists in the dictionary is added, it's removed from
        the dictionary.
        After everything has been removed, the provided project path is added to the dictionary (assuming it
        is not NULL).

        Args:
            pklpath (path/str): the path `(or string of the path)` to the project file that's being updated.
        """     
        while len(self.recentlist) > 4:
            del self.recentlist[0]
        for recenttuple in self.recentlist:
            if pklpath and str(Path(pklpath).as_posix()) == recenttuple[0]:
                self.recentlist.remove(recenttuple)
        if pklpath:
            self.recentlist.append((str(Path(pklpath).as_posix()), 1))  

    def get_recent(self):
        """
        Makes and maintains a JSON file that stores a dictionary with project file paths.
        """
        if not os.path.isfile(self.RECENT_PATH):
            f = open(self.RECENT_PATH, "x")
            f.write("[]")
            f.close()
        with open(self.RECENT_PATH) as f:
            self.recentlist = list(dict(json.load(f)).items())

    def save_recent(self):
        """
        When exiting the app, saves the open recents directory of project file paths to the 
        JSON file so it's accessible and accurate with the same information the next time the
        app is opened.
        """
        with open(self.RECENT_PATH, 'w') as f:
            json.dump(self.recentlist, f)
            print("saved recent files.")