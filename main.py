import subprocess
import tkinter as tk           
from tkinter import font as tkfont  
#import scripts.getMeta as meta
from gui.PipelineGUI import PipelineGUI
from gui.StartGUI import StartGUI
from time import sleep
from threading import Thread    
import pathlib as pl
import scripts.dense2mesh as d2m

debug = False # while true, recon scripts will not be run

class main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Controller Variables
        self.projdir = ""
        self.imagedir = ""
        self.A = (0,0)
        self.B = (0,0)
        self.map = None
        self.image = None
        self.p = None

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
        self.projdir = projdir
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
        if debug:
            print("starting recon")
            sleep(5)
            print("recon complete")
            return
        else:
            image2dense = pl.Path("scripts/image2dense.bat").resolve()
            workingdir = image2dense.parent
            self.p = subprocess.Popen([str(image2dense), str(self.projdir), str(self.imagedir)], cwd=str(workingdir))
            self.page2.action.config(text="Cancel")
            self.page2.STATE = 1

        rcode = self.p.wait()
        if rcode == 0: # Start dense2mesh
            if d2m.dense2mesh(self.projdir): # true if exited normally
                self.page2.action.config(text="Export")
                self.page2.STATE = 2

    def add_photos(self, imagedir):
        self.imagedir = imagedir
        self.page2.setbounds.config(state="active")

    def set_bounds(self, A, B):
        self.page2.action.config(state="active")
        self.A = A
        self.B = B

    def start_recon(self):
        self.thread1 = Thread(target = self._recon)
        self.thread1.start()

    def cancel_recon(self):
        if debug:
            print("canceling recon")
            return
        else:
            try:
                d2m.kill()
                self.p.terminate()  # Attempt to gracefully terminate
                self.p.wait(timeout=5)  # Wait for the process to finish (with timeout)
            except subprocess.TimeoutExpired:
                self.p.kill()  # Forcefully kill if terminate() didn't work

            self.page2.action.config(text="Start")
            self.page2.STATE = 0

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