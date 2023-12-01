import pickle
import tkinter as tk       
from tkinter import font as tkfont  
from tkinter import messagebox as mb
from scripts.PhotoManager import PhotoManager
from gui.PipelineGUI import PipelineGUI
from gui.StartGUI import StartGUI
import threading   
import pathlib as pl

from scripts.ReconManger import ReconManager

# DEBUG = True will cause the application to skip over recon scripts for testing
DEBUG = False

class main(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Controller Variables
        self.projdir = None
        self.imgdir = None
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

    # Common startur tasks for both opening and creating projects
    def _startup(self):
        self.page2 = PipelineGUI(self.container, self, self.projdir)
        self.page2.grid(row=0, column=0, sticky="nsew")
        self.page2.set_map(self.page2.DEFAULT_MAP)
        self.page2.set_example_image(self.page2.DEFAULT_PREVIEW)
        self.page2.tkraise()

        photomanager = PhotoManager(self.imgdir)
        photomanager.make_dict()

        self.page2.matcher.config(state="active")
        self.page2.update_text(numimg=photomanager.numimg)
        self.recon = ReconManager(self, self.imgdir, self.projdir)

    # Handler for creating of a new project
    #   Create a PipelineGUI object and load it onto the application
    def new_project(self, projdir):
        self.projdir = pl.Path(projdir)
        self._startup()
        
    # Handler for loading an existing project
    #   Method should read a project save file and create a PipelineGUI object
    def open_project(self, projfile):
        # Load the path variables from the file
        with open(projfile, 'rb') as file:
            self.projdir, self.imgdir = pickle.load(file)
        self._startup()

        # TODO: Check to see if there is already a fused.ply and if there is allow the user to start mesher

    # Handler for adding photos
    #   Set the controller variable for image directory
    #   This method should not open a dialogue, the is the role of the GUI classes
    def add_photos(self, imgdir):
        self.imgdir = pl.Path(imgdir)

        # Save the project paths to a file
        with open(self.projdir / pl.Path('project.pkl'), 'wb') as file:
            pickle.dump((self.projdir, self.imgdir), file)

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
        self.thread1 = threading.Thread(target = self.recon.recon_matcher)
        self.thread1.daemon = True
        self.thread1.start()

    # Handler for starting recon
    #   Start a new thread with the _recon() method
    def start_mesher(self):
        self.thread1 = threading.Thread(target = self.recon.recon_mesher)
        self.thread1.daemon = True
        self.thread1.start()

    # Hanlder for canceling recon
    #   Should kill any active subprocess as well as set the kill flag in dense2mesh.py
    #   After cancel it should change the action button back to start
    def cancel_recon(self):
        self.recon.cancel()
    
    # Handler for exporting final project:
    #   Should open a new dialogue with instructions for connecting headset
    #   and loading mesh+texture onto quest 2
    def export(self):
        if not DEBUG:
            print("PLACEHOLDER")
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
    if app.p:
        app.p.terminate()
