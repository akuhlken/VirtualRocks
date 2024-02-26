from pathlib import Path
import json
import os

# TODO: add comments for things, probs wait until we understand what the auto-documentation wants.

class RecentsManager():

    RECENT_PATH = Path('gui/recents.json')

    def __init__(self):
        """
        description about the whole class
        """
        self.recentlist = self.get_recent() 

    def update_recent(self, pklpath):    
        """
        description

        Args:
            pklpath (int): what is it?
        """     
        while len(self.recentlist) > 4:
            del self.recentlist[0]
        for rectup in self.recentlist:
            if pklpath and str(Path(pklpath).as_posix()) == rectup[0]:
                self.recentlist.remove(rectup)
        if pklpath:
            self.recentlist.append((str(Path(pklpath).as_posix()), 1))  

    def get_recent(self):
        """
        description
        """
        if not os.path.isfile(self.RECENT_PATH):
            f = open(self.RECENT_PATH, "x")
            f.write("[]")
            f.close()
        with open(self.RECENT_PATH) as f:
            self.recentlist = list(dict(json.load(f)).items())

    def save_recent(self):
        with open(self.RECENT_PATH, 'w') as f:
            json.dump(self.recentlist, f)
            print("saved recent files.")