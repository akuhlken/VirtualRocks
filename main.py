import os
import pickle
import shutil
import subprocess
import sys
import tkinter as tk       
from tkinter import font as tkfont  
from tkinter import messagebox as mb
from scripts.LogRedirect import LogRedirect
from scripts.PhotoManager import PhotoManager
from gui.PipelineGUI import PipelineGUI
from gui.StartGUI import StartGUI
from time import sleep
from threading import Thread    
import pathlib as pl

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

    # Handler for creating of a new project
    #   Create a PipelineGUI object and load it onto the application
    def new_project(self, projdir):
        self.page2 = PipelineGUI(self.container, self, projdir)
        self.projdir = pl.Path(projdir)
        self.page2.grid(row=0, column=0, sticky="nsew")
        self.page2.set_map(self.page2.DEFAULT_MAP)
        self.page2.set_example_image(self.page2.DEFAULT_PREVIEW)
        self.page2.tkraise()

        self.old_stdout = sys.stdout    
        sys.stdout = LogRedirect(self.page2.logtext)

    # Handler for loading an existing project
    #   Method should read a project save file and create a PipelineGUI object
    def open_project(self, projfile):
        # Load the path variables from the file
        with open(projfile, 'rb') as file:
            self.projdir, self.imgdir = pickle.load(file)
        self.page2 = PipelineGUI(self.container, self, self.projdir)
        self.page2.grid(row=0, column=0, sticky="nsew")
        self.page2.set_map(self.page2.DEFAULT_MAP)
        self.page2.set_example_image(self.page2.DEFAULT_PREVIEW)
        self.page2.tkraise()

        self.old_stdout = sys.stdout    
        sys.stdout = LogRedirect(self.page2.logtext)

        photomanager = PhotoManager(self.imgdir)
        self.page2.matcher.config(state="active")
        self.page2.update_text(numimg=photomanager.numimg)

    # Main matcher pipeling code
    #   NOTE: This method runs in its own thread
    #   method should run all scripts accosiated with Colmap and result
    #   in a desnse reconstruction
    def _recon_matcher(self):
        print()
        print("____________STARTING MATCHER____________")
        self.page2.state = 1 # state = in progress
        self.page2.matcher.config(text="Cancel")

        if PhotoManager(self.imgdir).numimg < 5:
            mb.showerror("Not enough images                           ")
            return

        if DEBUG:
            print("starting matcher")
            sleep(5)
            print("matching complete")
            self.page2.matcher.config(text="done")
            self.page2.matcher.config(state="disabled")
            self.page2.setbounds.config(state="active")
            self.page2.state = 2 # state = matcher done
            return

        # clean old database
        database = self.projdir / pl.Path(r"database.db")
        if os.path.exists(database):
            os.remove(database)
            print("removed old database")

        # Colmap recon
        colmap = pl.Path("scripts/COLMAP.bat").resolve()
        workingdir = colmap.parent
        self.p = subprocess.Popen([str(colmap), "feature_extractor", "--database_path", f"{self.projdir}\database.db", "--image_path", f"{self.imgdir}"], cwd=str(workingdir), stdout=subprocess.PIPE, bufsize=1, text=True)
        while self.p.poll() is None:
            msg = self.p.stdout.readline().strip() # read a line from the process output
            if msg:
                print(msg)
        rcode = self.p.wait()

        if rcode == 0:
            self.page2.progress.step(10)
            self.page2.progresstotal.step(1)
            self.p = subprocess.Popen([str(colmap), "exhaustive_matcher", "--database_path", f"{self.projdir}\database.db"], cwd=str(workingdir), stdout=subprocess.PIPE, bufsize=1, text=True)
            while self.p.poll() is None:
                msg = self.p.stdout.readline().strip() # read a line from the process output
                if msg:
                    print(msg)
            rcode = self.p.wait()

        if rcode == 0:
            self.page2.progress.step(10)
            self.page2.progresstotal.step(1)

            sparsedir = self.projdir / pl.Path(r"sparse")
            if os.path.exists(sparsedir):
                shutil.rmtree(sparsedir)
            os.makedirs(sparsedir)
        
            self.p = subprocess.Popen([str(colmap), "mapper", "--database_path", f"{self.projdir}\database.db", "--image_path", f"{self.imgdir}", "--output_path", f"{self.projdir}\sparse"], cwd=str(workingdir), stdout=subprocess.PIPE, bufsize=1, text=True)
            while self.p.poll() is None:
                msg = self.p.stdout.readline().strip() # read a line from the process output
                if msg:
                    print(msg)
            rcode = self.p.wait()

        if rcode == 0:
            self.page2.progress.step(10)
            self.page2.progresstotal.step(1)

            densedir = self.projdir / pl.Path(r"dense")
            if os.path.exists(densedir):
                shutil.rmtree(densedir)
            os.makedirs(densedir)

            self.p = subprocess.Popen([str(colmap), "image_undistorter", "--image_path", f"{self.imgdir}", "--input_path", rf"{self.projdir}\sparse\0", "--output_path", f"{self.projdir}\dense", "--output_type", "COLMAP", "--max_image_size", "2000"], cwd=str(workingdir), stdout=subprocess.PIPE, bufsize=1, text=True)
            while self.p.poll() is None:
                msg = self.p.stdout.readline().strip() # read a line from the process output
                if msg:
                    print(msg)
            rcode = self.p.wait()

        if rcode == 0:
            self.page2.progress.step(10)
            self.page2.progresstotal.step(1)

            self.p = subprocess.Popen([str(colmap), "patch_match_stereo", "--workspace_path", f"{self.projdir}\dense", "--workspace_format", "COLMAP", "--PatchMatchStereo.geom_consistency", "true"], cwd=str(workingdir), stdout=subprocess.PIPE, bufsize=1, text=True)
            while self.p.poll() is None:
                msg = self.p.stdout.readline().strip() # read a line from the process output
                if msg:
                    print(msg)
            rcode = self.p.wait()

        if rcode == 0: 
            self.page2.progress.step(10)
            self.page2.progresstotal.step(1)
            self.p = subprocess.Popen([str(colmap), "stereo_fusion", "--workspace_path", f"{self.projdir}\dense", "--workspace_format", "COLMAP", "--input_type", "geometric", "--output_path", rf"{self.projdir}\dense\fused.ply"], cwd=str(workingdir), stdout=subprocess.PIPE, bufsize=1, text=True)
            while self.p.poll() is None:
                msg = self.p.stdout.readline().strip() # read a line from the process output
                if msg:
                    print(msg)
            rcode = self.p.wait()

        if rcode == 0: 
            self.page2.progress.step(10)
            self.page2.progresstotal.step(1)
            self.p = subprocess.Popen([str(colmap), "model_converter", "--input_path", rf"{self.projdir}\dense\sparse", "--output_path", f"{self.projdir}\dense\images\project", "--output_type", "Bundler"], cwd=str(workingdir), stdout=subprocess.PIPE, bufsize=1, text=True)
            while self.p.poll() is None:
                msg = self.p.stdout.readline().strip() # read a line from the process output
                if msg:
                    print(msg)
            rcode = self.p.wait()

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
        print()
        print("____________STARTING MESHER____________")
        self.page2.state = 3
        self.page2.mesher.config(text="Cancel")
        if DEBUG:
            print("starting mesher")
            sleep(5)
            print("meshing complete")
            self.page2.mesher.config(text="Export")
            self.page2.state = 4
            return
        
        colmap = pl.Path("scripts/COLMAP.bat").resolve()
        workingdir = colmap.parent
        # TODO have next line run specific python version?
        self.p = subprocess.Popen(['python', 'Mesher.py', self.projdir], cwd=str(workingdir), stdout=subprocess.PIPE, bufsize=1, text=True)
        while self.p.poll() is None:
            msg = self.p.stdout.readline().strip() # read a line from the process output
            if msg:
                print(msg)
        rcode = self.p.wait()
        if rcode == 0:
            # If reconstruction exited normally
            self.page2.mesher.config(text="Export")
            self.page2.state = 4

    # Handler for adding photos
    #   Set the controller variable for image directory
    #   This method should not open a dialogue, the is the role of the GUI classes
    def add_photos(self, imgdir):
        self.imgdir = pl.Path(imgdir)

        # Save the project paths to a file
        with open(self.projdir / pl.Path('project.pkl'), 'wb') as file:
            pickle.dump((self.projdir, self.imgdir), file)

        photomanager = PhotoManager(self.imgdir)
        photomanager.make_dict()

        self.page2.matcher.config(state="active")
        self.page2.update_text(numimg=photomanager.numimg)

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
        if DEBUG:
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
    sys.stdout = app.old_stdout
