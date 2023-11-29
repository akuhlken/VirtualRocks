import os
import subprocess
import tkinter as tk       
from pprint import pprint    
from tkinter import font as tkfont  
from scripts.PhotoManager import PhotoManager
from gui.PipelineGUI import PipelineGUI
from gui.StartGUI import StartGUI
from time import sleep
from threading import Thread    
import pathlib as pl

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
        print("PLACEHOLDER")

    # Main matcher pipeling code
    #   NOTE: This method runs in its own thread
    #   method should run all scripts accosiated with Colmap and result
    #   in a desnse reconstruction
    def _recon_matcher(self):
        self.page2.state = 1 # state = in progress
        self.page2.matcher.config(text="Cancel")
        if debug:
            print("starting matcher")
            sleep(5)
            print("matching complete")
            self.page2.matcher.config(text="done")
            self.page2.matcher.config(state="disabled")
            self.page2.setbounds.config(state="active")
            self.page2.state = 2 # state = matcher done
            return

        # Colmap recon
        colmap = pl.Path("scripts/COLMAP.bat").resolve()
        workingdir = colmap.parent
        self.p = subprocess.Popen([str(colmap), "feature_extractor", "--database_path", f"{self.projdir}\database.db", "--image_path", f"{self.imagedir}"], cwd=str(workingdir))
        rcode = self.p.wait()
        self.page2.progress.step(10)

        if rcode == 0: self.p = subprocess.Popen([str(colmap), "exhaustive_matcher", "--database_path", f"{self.projdir}\database.db"], cwd=str(workingdir))
        rcode = self.p.wait()
        # do progress stuff, can do in main: self.page2.progress
        self.page2.progress.step(10)

        sparsedir = self.projdir + r"\sparse"
        if not os.path.exists(sparsedir):
            os.makedirs(sparsedir)
    
        if rcode == 0: self.p = subprocess.Popen([str(colmap), "mapper", "--database_path", f"{self.projdir}\database.db", "--image_path", f"{self.imagedir}", "--output_path", f"{self.projdir}\sparse"], cwd=str(workingdir))
        rcode = self.p.wait()
        self.page2.progress.step(10)

        densedir = self.projdir + r"\dense"
        if not os.path.exists(densedir):
            os.makedirs(densedir)

        if rcode == 0: self.p = subprocess.Popen([str(colmap), "image_undistorter", "--image_path", f"{self.imagedir}", "--input_path", rf"{self.projdir}\sparse\0", "--output_path", f"{self.projdir}\dense", "--output_type", "COLMAP", "--max_image_size", "2000"], cwd=str(workingdir))
        rcode = self.p.wait()
        self.page2.progress.step(10)

        if rcode == 0: self.p = subprocess.Popen([str(colmap), "patch_match_stereo", "--workspace_path", f"{self.projdir}\dense", "--workspace_format", "COLMAP", "--PatchMatchStereo.geom_consistency", "true"], cwd=str(workingdir))
        rcode = self.p.wait()
        self.page2.progress.step(10)

        if rcode == 0: self.p = subprocess.Popen([str(colmap), "stereo_fusion", "--workspace_path", f"{self.projdir}\dense", "--workspace_format", "COLMAP", "--input_type", "geometric", "--output_path", rf"{self.projdir}\dense\fused.ply"], cwd=str(workingdir))
        rcode = self.p.wait()
        self.page2.progress.step(10)

        if rcode == 0: self.p = subprocess.Popen([str(colmap), "model_converter", "--input_path", rf"{self.projdir}\dense\sparse", "--output_path", f"{self.projdir}\dense\images\project", "--output_type", "Bundler"], cwd=str(workingdir))
        rcode = self.p.wait()
        self.page2.progress.step(10)

        if rcode == 0:
            self.page2.matcher.config(text="done")
            self.page2.matcher.config(state="disabled")
            self.page2.setbounds.config(state="active")
            self.page2.state = 2 # state = matcher done
            self.page2.progress.stop()

    # Main mesher pipeling code
    #   NOTE: This method runs in its own thread
    #   method should run the point filtering and then dense2mesh scripts
    #   TODO: This is where the point filtering will happen using the user bounds
    def _recon_mesher(self):
        self.page2.state = 3
        self.page2.mesher.config(text="Cancel")
        if debug:
            print("starting mesher")
            sleep(5)
            print("meshing complete")
            self.page2.mesher.config(text="Export")
            self.page2.state = 4
            return
        
        dense2mesh = pl.Path("scripts/COLMAP.bat").resolve()
        workingdir = dense2mesh.parent
        # TODO have next line run specific python version?
        self.p = subprocess.Popen(['python', 'dense2mesh.py', self.projdir], cwd=str(workingdir))
        rcode = self.p.wait()
        if rcode == 0:
            # If reconstruction exited normally
            self.page2.mesher.config(text="Export")
            self.page2.state = 4

    # Handler for adding photos
    #   Set the controller variable for image directory
    #   This method should not open a dialogue, the is the role of the GUI classes
    def add_photos(self, imagedir):
        self.imagedir = imagedir
        self.photomanager = PhotoManager(self.imagedir)
        self.photomanager.make_dict()

        self.page2.matcher.config(state="active")
        self.page2.update_text(numimg=self.photomanager.numimg)

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
                self.p.terminate() 
                self.p.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.p.kill() 
        
        if self.page2.state == 1:
            self.page2.matcher.config(text="Start Matcher")
            self.page2.state = 0
        if self.page2.state == 3:
            self.page2.mesher.config(text="Start Mesher")
            self.page2.state = 2
    
    # Handler for exporting final project:
    #   Should open a new dialogue with instructions for connecting headset
    #   and loading mesh+texture onto quest 2
    def export(self):
        if not debug:
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