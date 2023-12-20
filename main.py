import pickle
import tkinter as tk   
import ttkbootstrap as tttk   
from tkinter import ttk
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
        self.image = None
        self.recon = None

        # Configuration variables
        self.minsize(500, 300)
        self.geometry("1000x700")
        self.title("VirtualRocks")
        icon = tk.PhotoImage(file=pl.Path(r"gui\placeholder\logo.png").resolve())
        self.iconphoto(True, icon)

        # Application styling
        self.buttoncolor = "#ffffff"  # for the buttons on page 1
        self.backcolor = "#ffffff"  # background of map + menu bar
        self.logbackground = "#ffffff"
        self.style = tttk.Style("darkly")

        #self.style.theme_use('xpnative')

        # maybe look into resize stuff? might be too hard
        self.style.configure("TButton", width=16)
        self.style.configure("cancel.TButton", width=30)
        #self.style.configure("TLabel", background="#ffffff")
        self.style.configure("title.TLabel", font=('Helvetica', 30, "bold"))
        #self.style.configure("TFrame", background="#ffffff")

        # Progress bar styling
        #self.style.element_create("color.pbar", "from", "xpnative") # for coloring the bar
        self.style.layout("prog.Horizontal.TProgressbar",
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar', {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}),
              ('Horizontal.Progressbar.label', {'sticky': ''})])
        self.style.configure("prog.Horizontal.TProgressbar", font=('Helvetica', 11), background="goldenrod1")
        #self.style.configure(self.style_name, background=BarColor[0], troughcolor=BarColor[1],
         #                   troughrelief=relief, borderwidth=border_width, thickness=width)


        # container is a stack of frames (aka our two main pages)
        self.container = ttk.Frame(self)
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
        self.recon = ReconManager(self, self.projdir)

    # Handler for creating of a new project
    #   Create a PipelineGUI object and load it onto the application
    def new_project(self, projdir):
        print("creating new project")
        self.projdir = pl.Path(projdir)
        self._startup()
        self.page2.dirtext.config(text=f"PATH: [ {self.projdir} ]")
        
    # Handler for loading an existing project
    #   Method should read a project save file and create a PipelineGUI object
    def open_project(self, projfile):
        print("opening project")
        # Load the path variables from the file
        self.projdir = pl.Path(projfile).parent
        with open(projfile, 'rb') as file:
            path = pickle.load(file)
        if path.is_absolute():
            self.imgdir = path
        else:
            self.imgdir = self.projdir / path
        self._startup() 
        self.page2.dirtext.config(text=f"PATH: [ {self.projdir} ]")
        try:
            pm = PhotoManager(self.imgdir)
            self.page2.update_text(pm.numimg)
            self.page2.set_example_image(self.imgdir / pl.Path(pm.get_example()))

            self.page2.matcher.config(state="active")

            if (self.projdir / pl.Path(r"dense\fused.ply")).is_file():
                self.page2.setbounds.config(state="active")

            if (self.projdir / pl.Path(r"out\100k.obj")).is_file():
                self.page2.setbounds.config(state="active")
                self.page2.mesher.config(state="active")
                self.page2.export.config(state="active")
            self.page2.progresstotal.step()
        except Exception as e:
            self.recon._send_log("Could not find image directory")
            print(e)
        
    # Handler for adding photos
    #   Set the controller variable for image directory
    #   This method should not open a dialogue, the is the role of the GUI classes
    def add_photos(self, imgdir):
        self.recon._send_log("$$$")
        self.recon._send_log("$.Image Loading.0$")
        self.projdir.resolve()
        self.imgdir = pl.Path(imgdir).resolve()
        try:
            path = self.imgdir.relative_to(self.projdir)
            self.recon._send_log("Created savefile with project paths")
        except:
            path = self.imgdir
            self.recon._send_log("Photos directory is not a sub-directory of project")
            self.recon._send_log("Saving as absolute path...")
        # Save the project paths to a file
        with open(self.projdir / pl.Path('project.pkl'), 'wb') as file:
            pickle.dump((path), file)
        pm = PhotoManager(self.imgdir)
        self.recon._send_log("$Image Loading..100$")
        self.page2.update_text(pm.numimg)
        self.page2.set_example_image(self.imgdir / pl.Path(pm.get_example()))
        self.page2.matcher.config(state="active")
        self.page2.setbounds.config(state="disabled")
        self.page2.mesher.config(state="disabled")
        self.page2.export.config(state="disabled")
            
    # Handler for seeting the project bounds
    #   Set the controller variables acording to bounds specified by the user
    #   This method should not open a dialogue, the is the role of the GUI classes
    def set_bounds(self, A, B):
        self.recon._send_log("$$")
        self.recon._send_log("$Setting Bounds..100$")
        self.page2.mesher.config(state="active")
        self.page2.export.config(state="disabled")
        self.A = A
        self.B = B

    # Handler for starting recon
    #   Start a new thread with the _recon() method
    def start_matcher(self):
        self.recon.imgdir = self.imgdir
        self.page2.setbounds.config(state="disabled")
        self.page2.mesher.config(state="disabled")
        self.page2.export.config(state="disabled")
        self.thread1 = threading.Thread(target = self.recon.matcher)
        self.thread1.daemon = True
        self.thread1.start()

    # Handler for starting recon
    #   Start a new thread with the _recon() method
    def start_mesher(self):
        self.recon.imgdir = self.imgdir
        self.page2.export.config(state="disabled")
        self.thread1 = threading.Thread(target = self.recon.mesher)
        self.thread1.daemon = True
        self.thread1.start()

    # Hanlder for canceling recon
    #   Should kill any active subprocess as well as set the kill flag in dense2mesh.py
    #   After cancel it should change the action button back to start
    def cancel_recon(self):
        self.recon.cancel()

    # Handler for setting dark mode
    #   changes theme to a dark theme
    def start_darkmode(self):
        self.recon._send_log("Changing app style to dark mode...")
        self.style = tttk.Style("darkly")
        self.page2.set_map(pl.Path(f"gui/placeholder/darkmap.jpg").resolve())

    def start_lightmode(self):
        self.recon._send_log("Changing app style to light mode...")
        self.style = tttk.Style("lumen")
        self.style.configure("TButton", width=16)
        self.style.configure("cancel.TButton", width=30)
        self.page2.set_map(pl.Path(f"gui/placeholder/map.jpg").resolve())

    
    # Handler for exporting final project:
    #   Should open a new dialogue with instructions for connecting headset
    #   and loading mesh+texture onto Quest 2
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

    def _shutdown(self):
        try:
            self.recon.cancel()
        except:
            print("no active processes")
        print("exiting app")
        self.destroy()

if __name__ == "__main__":
    app = main()
    app.protocol("WM_DELETE_WINDOW", app._shutdown)
    app.mainloop()
