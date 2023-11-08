import subprocess
import tkinter as tk           
from tkinter import font as tkfont  
#import scripts.getMeta as meta
from gui.PipelineGUI import PipelineGUI
from gui.StartGUI import StartGUI
from time import sleep
from threading import Thread    
from os import system

debug = False # while true, recon scripts will not be run

class main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Controller Variables
        self.projfile = ""
        self.imagedir = ""
        self.A = (0,0)
        self.B = (0,0)
        self.map = None
        self.image = None

        self.minsize(500, 300)
        self.geometry("1000x500")
        self.title("VirtualRocks")

        # Application styling
        self.font = tkfont.Font(family='Arial', size=24, weight="bold")
        self.buttoncolor = "#ffffff"
        self.backcolor = "#ffffff"

        # container is a stack of fames (aka out two main pages)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.page1 = StartGUI(parent=self.container, controller=self)
        self.page1.grid(row=0, column=0, sticky="nsew")
        self.page1.tkraise()

    def new_project(self, projdir):
        # TODO: self.projfile = progjdir + new file
        self.page2 = PipelineGUI(self.container, self, projdir)
        self.page2.grid(row=0, column=0, sticky="nsew")
        self.page2.set_map(self.page2.DEFAULT_MAP)
        self.page2.set_example_image(self.page2.DEFAULT_PREVIEW)
        self.page2.tkraise()

    def open_project(self, projfile):
        # TODO: loading of old project
        print("NOT YET COMPLETED")

    def _recon(self):
        self.page2.STATE = 1
        self.page2.action.config(text="Cancel")
        if not debug:
            subprocess.call(r"C:\Users\akuhl\Desktop\GitHub\VirtualRocks\scripts\image2dense.bat", shell=True)
        else:
            print("starting recon")
            sleep(5)
            print("recon complete")
        self.page2.action.config(text="Export")
        self.page2.STATE = 2

    def add_photos(self, imagedir):
        pass
        self.page2.setbounds.config(state="active")

    def set_bounds(self, A, B):
        self.page2.action.config(state="active")
        self.A = A
        self.B = B

    def start_recon(self):
        # both of these get a permission denied error

        #subprocess.call(["/home/kuhlkena/Documents/GitHub/VirtualRocks/scripts/temp.py"])
        #system("/home/kuhlkena/Documents/GitHub/VirtualRocks/scripts/temp.py")
        self.thread1 = Thread(target = self._recon)
        self.thread1.start()

    def cancel_recon(self):
        # TODO: kill self.thread1
        if not debug:
            pass # TODO: cancel recon
        else:
            print("canceling recon")
        #self.page2.action.config(text="Start")

    def export(self):
        if not debug:
            pass # TODO: export model
        else:
            print("Exported")

    def update_log(self):
        pass

    def update_progress(self):
        pass

    def update_map(self):
        pass

if __name__ == "__main__":
    app = main()
    app.mainloop()