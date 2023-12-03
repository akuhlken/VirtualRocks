import os
import shutil
import subprocess
import tkinter as tk       
from scripts.PhotoManager import PhotoManager
import pathlib as pl

class ReconManager():

    def __init__(self, controller, imgdir, projdir):
        self.controller = controller
        self.imgdir = imgdir
        self.projdir = projdir

    # Method for updating progress bar and progress text
    #   when a process completes messages should be sent in the form: "$nextstep$""
    #   To reset the progress bar, send message "$$"
    def _update_progress(self, msg):
        current = msg.replace('$', '')
        # TODO: Update progress and set progress text == curent
        if current == "":
            pass
            # TODO: reset progress bar

    # Method has two behaviors, if passed a string this method will act like a print() to the log
    #   if no args are provided this will capture any messages that self.p sends and send them to the log,
    #   returning when self.p finishes
    def _send_log(self, msg=None):
        if msg:
            self.controller.page2.logtext.insert(tk.END, msg + "\n")
            self.controller.page2.logtext.see("end")
            #if msg[0] == '$' and msg[-1] == '$':
                    #self._update_progress(msg)
            return
        while self.p.poll() is None:
            msg = self.p.stdout.readline().strip() # read a line from the process output
            if msg:
                self.controller.page2.logtext.insert(tk.END, msg + "\n")
                self.controller.page2.logtext.see("end")
                #if msg[0] == '$' and msg[-1] == '$':
                    #self._update_progress(msg)

        
    # Main matcher pipeling code
    #   NOTE: This method runs in its own thread
    #   method should run all scripts accosiated with Colmap and result
    #   in a desnse reconstruction
    def matcher(self):
        try:
            if self.p:
                self.cancel()
        except:
            pass
        self._send_log("__________Starting Matcher__________")
        rcode = 0
        # clean old database
        try:
            database = self.projdir / pl.Path(r"database.db")
            if os.path.exists(database):
                os.remove(database)
        except:
            rcode = 1
            self._send_log("Database already open (wait for old process to exit)")

        # Colmap recon
        colmap = pl.Path("scripts/COLMAP.bat").resolve()
        workingdir = colmap.parent
        if rcode == 0:
            self.p = subprocess.Popen([str(colmap), "feature_extractor", "--database_path", f"{self.projdir}\database.db", "--image_path", f"{self.imgdir}"], cwd=str(workingdir), stdout=subprocess.PIPE, text=True)
            self._send_log()
            rcode = self.p.wait()

        if rcode == 0:
            self.controller.page2.progress.step(1)
            self.p = subprocess.Popen([str(colmap), "exhaustive_matcher", "--database_path", f"{self.projdir}\database.db"], cwd=str(workingdir), stdout=subprocess.PIPE, text=True)
            self._send_log()
            rcode = self.p.wait()

        if rcode == 0:
            try:
                sparsedir = self.projdir / pl.Path(r"sparse")
                if os.path.exists(sparsedir):
                    shutil.rmtree(sparsedir)
                os.makedirs(sparsedir)
            except:
                rcode = 1
                self._send_log("Database already open (wait for old process to exit)")

        if rcode == 0:
            self.controller.page2.progress.step(1)
            self.p = subprocess.Popen([str(colmap), "mapper", "--database_path", f"{self.projdir}\database.db", "--image_path", f"{self.imgdir}", "--output_path", f"{self.projdir}\sparse"], cwd=str(workingdir), stdout=subprocess.PIPE, text=True)
            self._send_log()
            rcode = self.p.wait()

        if rcode == 0:
            try:
                densedir = self.projdir / pl.Path(r"dense")
                if os.path.exists(densedir):
                    shutil.rmtree(densedir)
                os.makedirs(densedir)
            except:
                rcode = 1
                self._send_log("Database already open (wait for old process to exit)")
    
        if rcode == 0:
            self.controller.page2.progress.step(1)
            self.p = subprocess.Popen([str(colmap), "image_undistorter", "--image_path", f"{self.imgdir}", "--input_path", rf"{self.projdir}\sparse\0", "--output_path", f"{self.projdir}\dense", "--output_type", "COLMAP", "--max_image_size", "2000"], cwd=str(workingdir), stdout=subprocess.PIPE, text=True)
            self._send_log()
            rcode = self.p.wait()

        if rcode == 0:
            self.controller.page2.progress.step(1)
            self.p = subprocess.Popen([str(colmap), "patch_match_stereo", "--workspace_path", f"{self.projdir}\dense", "--workspace_format", "COLMAP", "--PatchMatchStereo.geom_consistency", "true"], cwd=str(workingdir), stdout=subprocess.PIPE, text=True)
            self._send_log()
            rcode = self.p.wait()

        if rcode == 0: 
            self.controller.page2.progress.step(1)
            self.p = subprocess.Popen([str(colmap), "stereo_fusion", "--workspace_path", f"{self.projdir}\dense", "--workspace_format", "COLMAP", "--input_type", "geometric", "--output_path", rf"{self.projdir}\dense\fused.ply"], cwd=str(workingdir), stdout=subprocess.PIPE, text=True)
            self._send_log()
            rcode = self.p.wait()

        if rcode == 0: 
            self.controller.page2.progress.step(1)
            self.p = subprocess.Popen([str(colmap), "model_converter", "--input_path", rf"{self.projdir}\dense\sparse", "--output_path", f"{self.projdir}\dense\images\project", "--output_type", "Bundler"], cwd=str(workingdir), stdout=subprocess.PIPE, text=True)
            self._send_log()
            rcode = self.p.wait()

        if rcode == 0:
            self.controller.page2.setbounds.config(state="active")
            self.controller.page2.cancel.config(state="disabled")
            self.controller.page2.progress.config(value=6)
            self.controller.page2.progresstotal.step(9)
        self.p = None

    # Main mesher pipeling code
    #   NOTE: This method runs in its own thread
    #   method should run the point filtering and then dense2mesh scripts
    #   TODO: This is where the point filtering will happen using the user bounds
    def mesher(self):
        try:
            if self.p:
                self.cancel()
        except:
            pass
        self._send_log("__________Starting Mesher__________")
        
        colmap = pl.Path("scripts/COLMAP.bat").resolve()
        workingdir = colmap.parent
        # TODO have next line run specific python version?
        self.p = subprocess.Popen(['python', 'Mesher.py', self.projdir], cwd=str(workingdir), stdout=subprocess.PIPE, text=True, bufsize=1024)
        self._send_log()
        rcode = self.p.wait()
        if rcode == 0:
            # If reconstruction exited normally
            self.controller.page2.export.config(state="active")
            self.controller.page2.cancel.config(state="disabled")
        self.p = None

    #  Methods for canceling current recon
    #   Should kill any active subprocess as well as set the kill flag in dense2mesh.py
    #   After cancel it should change the action button back to start
    def cancel(self):
        self.controller.page2.cancel.config(state="disabled")
        if self.p:
            try:
                self.p.terminate() 
                self.p.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.p.kill()
        self._send_log("process was killed")
