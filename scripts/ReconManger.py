import os
import shutil
import subprocess
from pathlib import Path
from tkinter import messagebox as mb
import scripts.PointCloudManager as pcm

# Progress Constants
STARTED = 0
PHOTOS = 10
MATCHER = 70
MESHER = 100

# Path to specific python version installed by the installer
PYTHONPATH = os.getenv('LOCALAPPDATA') + "\\Programs\\Python\\Python311\\python.exe"

class ReconManager():

    def __init__(self, controller, projdir):
        """
        `ReconManager` is a controller class that manages the subprocesses for the 
        :ref:`Matcher <matcher>` and :ref:`Mesher <mesher>`. It also manages the progress bar
        displayed with projects on the Tk app.

        Args:
            controller (:ref:`Main <main>`): Reference to the main TK app
            projdir (pathlib.Path): Project directory containing .vrp file
        """
        self.controller = controller
        self.imgdir = None
        self.projdir = projdir
        self.progresspercent = 0
        self._update_progress("$$")

    def matcher(self):
        """
        Method for starting the subprocess for the matcher, runs :ref:`Matcher.py <matcher>` and
        updates application state after running. Prompts the user on whether or not to overwrite
        database if one exists.
        """
        clean = 'T'
        if (self.projdir / Path(r"database.db")).is_file():
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
        self.controller.update_state(PHOTOS)
        self.controller.page2.cancel.config(state="active")
        self._send_log("__________Starting Matcher__________")
        colmap = Path("scripts/COLMAP.bat").resolve()
        workingdir = colmap.parent
        self.p = subprocess.Popen([PYTHONPATH, 'Matcher.py', self.projdir, self.imgdir, clean], cwd=str(workingdir), stdout=subprocess.PIPE, text=True)
        self._send_log()
        rcode = self.p.wait()
        if rcode == 0:
            if Path(self.projdir / "dense" / "fused.ply").is_file(): # If reconstruction exited normally
                dense = Path(self.projdir / "dense")
                pcm.create_heat_map(Path(dense / "fused.ply"), dense)
                savefile = Path(dense / "save.ply")
                if os.path.isfile(savefile):
                    os.remove(savefile)
                shutil.copy(Path(dense / "fused.ply"), savefile)
                self.controller.update_state(MATCHER)
                self.controller.page2.cancel.config(state="disabled")
            else:
                self._send_log("Matcher failed, please retry")
        self.p = None

    def mesher(self):
        """
        Method for starting the subprocess for the mesher, runs :ref:`Mesher.py <mesher>` and
        updates application state after running.
        """
        try:
            if self.p:
                self.cancel()
        except:
            pass
        self.controller.update_state(MATCHER)
        self.controller.page2.cancel.config(state="active")
        self._send_log("__________Starting Mesher__________")
        colmap = Path("scripts/COLMAP.bat").resolve()
        workingdir = colmap.parent
        self.p = subprocess.Popen([PYTHONPATH, 'Mesher.py', self.projdir], cwd=str(workingdir), stdout=subprocess.PIPE, text=True)
        self._send_log()
        rcode = self.p.wait()
        if rcode == 0:
            if (self.projdir / Path(r"out\low_poly.obj")).is_file(): # If reconstruction exited normally
                self.controller.update_state(MESHER)
                self.controller.page2.cancel.config(state="disabled")
            else:
                self._send_log("Mesher failed, please retry")

    def cancel(self):
        """
        If a subprocess exists, this method sends teminate signal to current subprocess. After a
        timeout, the process will be sent a kill signal `(if it hasn't already terminated on its
        own)`. 

        .. note:: 
            When cancelling COLMAP, it may continue to run in the background and would no longer be
            tracked by the app. Additionally, if the user runs matcher back to back, the processes
            may conflict. To fix both of these issues, go to Task Manager, find the ``colmap.exe``
            task and manually end/kill it.
        """
        self.controller.page2.cancel.config(state="disabled")
        try:
            try:
                self.p.terminate()
                self.p.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.p.kill()
        except:
            pass
        self._send_log("process was sent kill signal")
        self._send_log("$$")

    def auto(self):
        """
        Method runs a full reconstruction from images to tiled meshes automatically.

        .. warning::  
            Using this method does not allow the user to trim point cloud. It's useful when running
            the app on a large dataset or overnight, but will likely result in a final mesh that 
            includes outlier points.
        """
        self.matcher()
        if (self.projdir / Path(r"dense\fused.ply")).is_file(): 
            self.mesher()

    def _update_progress(self, msg):
        """
        Helper method for updating the progress bar text and completion.

        The message (msg) input should be in the format `"$text1.text2.50$"`. 
        
        **text1** is the current step, and **text2** is the current substep being run `(text2 can
        be left blank if there is no substep)`. The text portions of the message will be displayed
        above the lower progress bar.
        
        The **number** is the percentage fill of the lower progress bar when the
        current step/substep combination begins. 

        Sending the message **"$$"** will reset the bar and text. 

        Args:
            msg (string): a string of form `"$text1.text2.int$"`
        """
        if msg == "$$":
            self.controller.page2.progress.stop()
            self.controller.style.configure('prog.Horizontal.TProgressbar', text='')
            self.controller.page2.progresstext.config(text=f"Nothing's running...")
            return
        pkg = msg.replace('$', '').split('.')
        currentstep = pkg[0]
        currentsubstep = pkg[1]
        percent = pkg[2]
        self.progresspercent = int(int(percent)/self.controller.page2.progress["maximum"] * 100)
        if currentsubstep == "":
            self.controller.page2.progresstext.config(text=f"Progress on {currentstep}: ")
        else:
            self.controller.page2.progresstext.config(text=f"Progress on {currentstep}, {currentsubstep}: ")
            currentstep = currentsubstep
        self.controller.style.configure('prog.Horizontal.TProgressbar', text='{:g} %'.format(self.progresspercent))
        self.controller.page2.progress.config(value=percent)
        if self.controller.page2.progress["value"] == self.controller.page2.progress["maximum"]:
            self.controller.page2.progresstext.config(text=f"{currentstep} complete!")
        
    def _send_log(self, msg=None):
        """
        Helper method to send a message to the :ref:`PipelineGUI <pipelineGUI>` log. If message
        starts and ends with **$**, it will go to the log and also be used to update the progress
        bar.

        If no message is provided, this method will wait for the current process to exit and
        will capture any messages sent through STDOUT by that process.

        Args:
            msg (string): Optional string to send to log
        """
        if msg:
            self.controller.page2.log(msg)
            if msg[0] == '$' and msg[-1] == '$':
                    self._update_progress(msg)
            return
        while self.p.poll() is None:
            msg = self.p.stdout.readline().strip() # read a line from the process output
            if msg:
                self.controller.page2.log(msg)
                if msg[0] == '$' and msg[-1] == '$':
                    self._update_progress(msg)