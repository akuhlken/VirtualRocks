import subprocess
import tkinter as tk       
import pathlib as pl
from tkinter import messagebox as mb

# Progress Constants
STARTED = 0
PHOTOS = 10
MATCHER = 70
MESHER = 100

class ReconManager():

    def __init__(self, controller, projdir):
        self.controller = controller
        self.imgdir = None
        self.projdir = projdir
        self.progresspercent = 0

    # Method for updating progress bar and progress text
    #   when a process completes messages should be sent in the form: "$nextstep$""
    #   To reset the progress bar, send message "$$"
    def _update_progress(self, msg):
        if msg == "$$":
            self.controller.page2.progress.stop()
            self.controller.style.configure('prog.Horizontal.TProgressbar', text='')
            self.controller.page2.progresstext.config(text=f"Nothing's running...")
            return
        
        elif msg == "$$$":
            self._update_progress("$$")
            return

        pkg = msg.replace('$', '').split('.')
        currentstep = pkg[0]
        currentsubstep = pkg[1]
        percent = pkg[2]
        self.progresspercent = int(int(percent)/self.controller.page2.progress["maximum"] * 100) # if we only use this variable once, is it worth keeping?
        if currentsubstep == "":
            self.controller.page2.progresstext.config(text=f"Progress on {currentstep}: ")
        else:
            self.controller.page2.progresstext.config(text=f"Progress on {currentstep}, {currentsubstep}: ")
            currentstep = currentsubstep
        self.controller.style.configure('prog.Horizontal.TProgressbar', text='{:g} %'.format(self.progresspercent))
        #self.controller.style.configure('Horizontal.Progressbar.label', text='{:g} %'.format(percentage))
        self.controller.page2.progress.config(value=percent)

        if self.controller.page2.progress["value"] == self.controller.page2.progress["maximum"]:
            self.controller.page2.progresstext.config(text=f"{currentstep} complete!")
        
    # Method has two behaviors, if passed a string this method will act like a print() to the log
    #   if no args are provided this will capture any messages that self.p sends and send them to the log,
    #   returning when self.p finishes
    def _send_log(self, msg=None):
        if msg:
            self.controller.page2.logtext.insert(tk.END, msg + "\n")
            self.controller.page2.logtext.see("end")
            if msg[0] == '$' and msg[-1] == '$':
                    self._update_progress(msg)
            return
        while self.p.poll() is None:
            msg = self.p.stdout.readline().strip() # read a line from the process output
            if msg:
                self.controller.page2.logtext.insert(tk.END, msg + "\n")
                self.controller.page2.logtext.see("end")
                if msg[0] == '$' and msg[-1] == '$':
                    self._update_progress(msg)

    # Main matcher pipeliningg code
    #   NOTE: This method runs in its own thread
    #   method should run all scripts accosiated with Colmap and result
    #   in a desnse reconstruction
    def matcher(self):
        clean = 'T'
        if (self.projdir / pl.Path(r"database.db")).is_file():
            response = mb.askyesnocancel("Start Matcher", "Start clean and remove old database?")
            if response == None:
                return
            if response == True:
                clean = 'T'
            if response == False:
                clean = 'F'

        try:
            if self.p:
                self.cancel()
        except:
            pass
        self.controller._update_state(PHOTOS)
        self.controller.page2.cancel.config(state="active")
        self._send_log("__________Starting Matcher__________")
        
        colmap = pl.Path("scripts/COLMAP.bat").resolve()
        workingdir = colmap.parent
        # TODO have next line run specific python version?
        # self.projdir, self.imgdir, clean
        self.p = subprocess.Popen(['python', 'Matcher.py', self.projdir, self.imgdir, clean], cwd=str(workingdir), stdout=subprocess.PIPE, text=True)
        self._send_log()
        rcode = self.p.wait()
        if rcode == 0:
            if (self.projdir / pl.Path(r"dense\fused.ply")).is_file():
            # If reconstruction exited normally
                self.controller._update_state(MATCHER)
                self.controller.page2.cancel.config(state="disabled")
            else:
                self._send_log("Matcher failed, please retry")
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
        self.controller._update_state(MATCHER)
        self.controller.page2.cancel.config(state="active")
        self._send_log("__________Starting Mesher__________")
        
        colmap = pl.Path("scripts/COLMAP.bat").resolve()
        workingdir = colmap.parent
        
        # TODO have next line run specific python version?
        self.p = subprocess.Popen(['python', 'Mesher.py', self.projdir], cwd=str(workingdir), stdout=subprocess.PIPE, text=True)
        self._send_log()
        rcode = self.p.wait()
        if rcode == 0:
            if (self.projdir / pl.Path(r"out\100k.obj")).is_file():
            # If reconstruction exited normally
                self.controller._update_state(MESHER)
                self.controller.page2.cancel.config(state="disabled")
            else:
                self._send_log("Mesher failed, please retry")

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
        self._send_log("process was sent kill signal")
        self._send_log("$$")

    # method to handle auto reconstruction without setting any user bounds
    def auto(self):
        self.matcher()
        if (self.projdir / pl.Path(r"dense\fused.ply")).is_file(): 
            self.mesher()