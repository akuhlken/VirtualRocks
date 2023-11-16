import subprocess
import tkinter as tk           
from tkinter import font as tkfont  
from gui.PipelineGUI import PipelineGUI
from gui.StartGUI import StartGUI
from time import sleep
from threading import Thread    
import pathlib as pl
import scripts.dense2mesh as d2m

# Debug = True will cause the application to skip over recon scripts for testing
debug = False

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

        # Configuration variables
        self.minsize(500, 300)
        self.geometry("1000x700")
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

        # Load staring page and start application
        self.page1 = StartGUI(parent=self.container, controller=self)
        self.page1.grid(row=0, column=0, sticky="nsew")
        self.page1.tkraise()

    # Handler for creating of a new project
    #   Create a PipelineGUI object and load it onto the application
    def new_project(self, projdir):
        self.page2 = PipelineGUI(self.container, self, projdir)
        self.projdir = projdir
        self.page2.grid(row=0, column=0, sticky="nsew")
        self.page2.set_map(self.page2.DEFAULT_MAP)
        self.page2.set_example_image(self.page2.DEFAULT_PREVIEW)
        self.page2.tkraise()

    # Handler for loading an existing project
    #   Method should read a project save file and create a PipelineGUI object
    def open_project(self, projfile):
        print("NO OPEN PROJECT FUNCTIONALITY")

    # Main matcher pipeling code
    #   NOTE: This method runs in its own thread
    #   method should sequentially run scripts involved in reconstruction
    #   Must keep track of wether scripts exited normally or were cancled
    #   and update button text and status
    def _recon_matcher(self):
        self.page2.state = 3 # state = in progress
        self.page2.matcher.config(text="Cancel")
        if debug:
            print("starting matcher")
            sleep(5)
            print("matching complete")
            self.page2.matcher.config(text="done")
            self.page2.matcher.config(state="disabled")
            self.page2.setbounds.config(state="active")
            self.page2.state = 1 # state = matcher done
            return

        image2dense = pl.Path("scripts/image2dense.bat").resolve()
        workingdir = image2dense.parent
        self.p = subprocess.Popen([str(image2dense), str(self.projdir), str(self.imagedir)], cwd=str(workingdir))
        rcode = self.p.wait()
        if rcode == 0:
            self.page2.matcher.config(text="done")
            self.page2.matcher.config(state="disabled")
            self.page2.setbounds.config(state="active")
            self.page2.state = 1 # state = matcher done

    # Main mesher pipeling code
    #   NOTE: This method runs in its own thread
    #   method should sequentially run scripts involved in reconstruction
    #   Must keep track of wether scripts exited normally or were cancled
    #   and update button text and status
    #   TODO: This is where the point filtering will happen
    def _recon_mesher(self):
        self.page2.state = 1
        self.page2.mesher.config(text="Cancel")
        if debug:
            print("starting mesher")
            sleep(5)
            print("meshing complete")
            self.page2.mesher.config(text="Export")
            self.page2.state = 2
            return

        if d2m.dense2mesh(self.projdir):
            # If reconstruction exited normally
            self.page2.mesher.config(text="Export")
            self.page2.state = 2

    # Handler for adding photos
    #   Set the controller variable for image directory
    #   This method should not open a dialogue, the is the role of the GUI classes
    def add_photos(self, imagedir):
        self.imagedir = imagedir
        self.page2.matcher.config(state="active")

    # Handler for seeting the project bounds
    #   Set the controller variables acording to bounds specified by the user
    #   This method should not open a dialogue, the is the role of the GUI classes
    def set_bounds(self, A, B):
        self.page2.mesher.config(state="active")
        self.A = A
        self.B = B

    # Handler for starting recon
    #   Start a new thread with the _recon() method
    def start_matcher(self):
        self.thread1 = Thread(target = self._recon_matcher)
        self.thread1.start()

    # Handler for starting recon
    #   Start a new thread with the _recon() method
    def start_mesher(self):
        self.thread1 = Thread(target = self._recon_mesher)
        self.thread1.start()

    # Hanlder for canceling recon
    #   Should kill any active subprocess as well as set the kill flag in dense2mesh.py
    #   After cancel it should change the action button back to start
    def cancel_recon(self):
        if debug:
            print("canceling recon")
            return
        else:
            try:
                d2m.kill()
                self.p.terminate() 
                self.p.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.p.kill() 
        
        if not self.page2.state == 1:
            self.page2.matcher.config(text="Start Matcher")
            self.page2.state = 0

        self.page2.mesher.config(text="Start Mesher")
        self.page2.state = 0
    
    
    # Handler for exporting final project:
    #   Should open a new dialogue with instructions for connecting headset
    #   and loading mesh+texture onto quest 2
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