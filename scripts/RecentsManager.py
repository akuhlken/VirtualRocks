from pathlib import Path
import json
import os

class RecentsManager():

    RECENT_PATH = Path('gui/recents.json')

    def __init__(self):
        self.recentlist = self.get_recent() 
        print(str(Path("placeholder/logo.png").absolute()))
        print(str(Path("StartGUI.py").resolve().parent))
        # try:
        #     # if no recents file exists yet, then make one
        #     f = open(Path("main.py").parent / 'recents.json', "x")
        #     f.write("[]")
        #     f.close()
        # except:
        #     # file already exist
        #     pass

    def update_recent(self, pklpath):         
        while len(self.recentlist) > 4:
            del self.recentlist[0]
        for rectup in self.recentlist:
            if pklpath and str(Path(pklpath).as_posix()) == rectup[0]:
                self.recentlist.remove(rectup)
        if pklpath:
            self.recentlist.append((str(Path(pklpath).as_posix()), 1))  

    def get_recent(self):
        # if no recent exists, then make one.
        if not os.path.isfile(self.RECENT_PATH):
            f = open(self.RECENT_PATH, "x")
            f.write("[]")
            f.close()
        with open(self.RECENT_PATH) as f:
            # need to check if empty? 
            self.recentlist = list(dict(json.load(f)).items())

    def save_recent(self):
        with open(self.RECENT_PATH, 'w') as f:
            json.dump(self.recentlist, f)
            print("saved recent files.")