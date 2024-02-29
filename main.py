import os
import shutil
import subprocess
from ttkbootstrap import Style
from tkinter import simpledialog, PhotoImage, Frame, Tk
from pathlib import Path
from threading import Thread
import  scripts.PhotoManager as pm
from gui.PipelineGUI import PipelineGUI
from gui.StartGUI import StartGUI
from scripts.ReconManger import ReconManager
import pickle
import ctypes
import scripts.PointCloudManager as PointCloudManager
from scripts.RecentsManager import RecentsManager

# Compiler run: pyinstaller --onefile main.py -w -p "scripts" -p "gui" -c
# After compiles move main.exe into the VirtualRocks directory

# DEBUG = True will cause the application to skip over recon scripts for testing
DEBUG = False

# Progress Constants
STARTED = 0
PHOTOS = 10
MATCHER = 70
MESHER = 100

class main(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Controller Variables
        self.projdir = None
        self.imgdir = ""
        self.recon = None
        self.state = STARTED
        self.fullscreen = False

        # Create recents
        self.recents = RecentsManager()
        self.recents.get_recent()

        # Sets app icon and identifier
        self.myappid = u'o7.VirtualRocks.PipelineApp.version-1.0' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(self.myappid)
        
        # Configuration variables
        self.projectname = "project"
        self.picklepath = ""
        self.minsize(500, 300)
        centerdim = self._open_middle(1000,700)
        self.geometry('%dx%d+%d+%d' % (1000, 700, centerdim[0], centerdim[1]))
        self.title("VirtualRocks")
        icon = PhotoImage(file=Path(r"gui\placeholder\logo.png").resolve())
        self.iconphoto(True, icon)

        # Application styling
        self.buttoncolor = "#ffffff"  # for the buttons on page 1
        self.logbackground = "#ffffff"
        self.style = Style("darkly")
        self.styleflag = "dark"

        # TODO: duplicate code? CODEN
        # setting initial style stuff (might be able to clean up bc this is just a copy from AppWindow.py)
        self.style.configure("TButton", width=16)
        self.style.configure("cancel.TButton", width=30)
        self.style.configure("title.TLabel", font=('Helvetica', 30, "bold"))

        # Progress bar styling
        self.style.layout("prog.Horizontal.TProgressbar",
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar', {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}),
              ('Horizontal.Progressbar.label', {'sticky': ''})])
        self.style.configure("prog.Horizontal.TProgressbar", font=('Helvetica', 11), background="goldenrod1")

        # container is a stack of frames (aka our two main pages)
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Load staring page and start application
        self.page1 = StartGUI(parent=self.container, controller=self, recents=self.recents)
        self.page1.grid(row=0, column=0, sticky="nsew")
        self.page1.tkraise()

        # Binding for fullscreen toggle
        self.bind("<F11>", self._toggle_fullscreen)
        self.bind("<Escape>", self._end_fullscreen)

    # Common startup tasks for both opening and creating projects
    def _startup(self):
        """
        description
        """
        self.page2 = PipelineGUI(self.container, self, self.projdir, self.recents)
        self.page2.grid(row=0, column=0, sticky="nsew")
        self.page2.set_example_image(self.page2.DEFAULT_PREVIEW)
        self.page2.tkraise()
        self.recon = ReconManager(self, self.projdir)
        self.page2.menubar.entryconfig("Reconstruction", state="normal")
        self.recents.update_recent(self.picklepath)

    # Handler for creating of a new project
    #   Create a PipelineGUI object and load it onto the application
    def new_project(self, projdir, name=None, imgdir=None):
        """
        description

        Args:
            projdir (type?): what is it?
            name (str): what is it?
            imgdir (type?): what is it?
        """
        print("creating new project")
        self.projdir = Path(projdir)
        if not name:
            self.projectname = simpledialog.askstring(title="Name Project As...", prompt="Enter a name for this project:", parent=self.page1, initialvalue=self.projectname)
        else:
            self.projectname = name
        self.picklepath = self.projdir / Path(self.projectname + '.pkl')
        self._startup()
        self.page2.dirtext.config(text=f"Workspace: [ {self.projdir} ]")
        self.title("VirtualRocks: " + self.projectname)
        if imgdir:
            self.imgdir = imgdir
            numimg = pm.get_num_img(imgdir)
            self.page2.update_text(numimg)
            self.page2.set_example_image(self.imgdir / Path(pm.get_example_img(imgdir)))
            if numimg > 0:
                self.update_state(PHOTOS)
        else:
            self.update_state(STARTED)
        
    # Handler for loading an existing project
    #   Method should read a project save file and create a PipelineGUI object
    def open_project(self, projfile):
        """
        description

        Args:
            projfile (type?): what is it?
        """
        print("opening project")
        self.picklepath = projfile
        self.projectname = Path(projfile).stem
        # Load the path variables from the file
        self.projdir = Path(projfile).parent
        with open(projfile, 'rb') as file:
            (path,self.state) = pickle.load(file)
        if Path(path).is_absolute():
            self.imgdir = path
        else:
            self.imgdir = self.projdir / path
        self._startup()
        self.update_state(self.state)
        self.title("VirtualRocks: " + self.projectname)
        self.page2.dirtext.config(text=f"Workspace: [ {self.projdir} ]")
        try:
            self.page2.update_text(pm.get_num_img(self.imgdir))
            self.page2.set_example_image(self.imgdir / Path(pm.get_example_img(self.imgdir)))
        except Exception as e:
            self.page2.log(str(e))
            self.page2.log("Could not find image directory")
            self.update_state(STARTED)

    # Handler for reopening the starting page
    #   since there's an option for it in the menu, it must be done.
    def back_to_start(self):
        """
        description
        """
        self.page1.tkraise()
        self.page2.menubar.entryconfig("Reconstruction", state="disabled")
        self.title("VirtualRocks")

    # Handler for adding photos
    #   Set the controller variable for image directory
    #   This method should not open a dialogue, the is the role of the GUI classes
    def add_photos(self, imgdir):
        """
        description

        Args:
            imgdir (type?): what is it?
        """
        self.recon._send_log("$$")
        self.recon._send_log("$.Image Loading.0$")
        self.projdir.resolve()
        self.imgdir = Path(imgdir).resolve()
        self.recon._send_log("$Image Loading..100$")
        numimg = pm.get_num_img(self.imgdir)
        self.page2.update_text(numimg)
        self.page2.set_example_image(self.imgdir / Path(pm.get_example_img(self.imgdir)))
        if numimg > 0:
            self.update_state(PHOTOS)

    # Removes points from dense point cloud as specified by bounds
    #   Handler in PipelineGUI creates dialog and passes bounds here
    def set_bounds(self, minx, maxx, miny, maxy):
        """
        description

        Args:
            minx (int): what is it?
            maxx (int): what is it?
            miny (int): what is it?
            maxy (int): what is it?
        """
        self.recon._send_log("$$")
        self.recon._send_log("$Trimming Bounds..100$")
        dense = Path(self.projdir / "dense")
        PointCloudManager.remove_points(Path(dense / "fused.ply"), minx, maxx, miny, maxy)
        PointCloudManager.create_heat_map(Path(dense / "fused.ply"), dense)
        self.page2.set_chart(Path(dense/ "heat_map.png"))

    # Handler for the restore point cloud menu item
    #   Should overwrite the current fused.ply with the un-edited save.ply
    #   Serves to undo the set bounds
    def restore(self):
        """
        description
        """
        if self.state >= MATCHER:
            dense = Path(self.projdir / "dense")
            savefile = Path(dense / "save.ply")
            shutil.copy(savefile, Path(dense / "fused.ply"))
            PointCloudManager.create_heat_map(Path(dense / "fused.ply"), dense)
            self.page2.set_chart(Path(dense/ "heat_map.png"))
        else:
            self.page2.log("Nothing to restore, run matcher to create a point cloud")

    # Handler for starting matcher
    #   Starts a new thread for the ReconManager.matcher() method
    def start_matcher(self):
        """
        description
        """
        self.recon.imgdir = self.imgdir
        self.thread1 = Thread(target = self.recon.matcher)
        self.thread1.daemon = True
        self.thread1.start()

    # Handler for starting mesher
    #   Starts a new thread for the ReconManager.mesher() method
    def start_mesher(self):
        """
        description
        """
        self.recon.imgdir = self.imgdir
        self.thread1 = Thread(target = self.recon.mesher)
        self.thread1.daemon = True
        self.thread1.start()

    # Handler for the automatic reconstruction feature
    #   Starts a new thread for the ReconManager.auto() method
    def auto_recon(self):
        """
        description
        """
        if not self.imgdir:
            self.page2.log("No images loaded")
            return
        self.recon.imgdir = self.imgdir
        self.thread1 = Thread(target = self.recon.auto)
        self.thread1.daemon = True
        self.thread1.start()

    # Handler for canceling recon
    #   Should call the recon managers cancel() method
    def cancel_recon(self):
        """
        description
        """
        self.recon.cancel()

    def preview_cloud(self):
        path = Path(self.projdir / 'dense' / 'fused.ply')
        p = subprocess.Popen(['python', 'scripts/CloudPreviewer.py', str(path)])

    # Method for updating the state of the application
    #   Should set the map image acordingly as well as activate and deactivate buttons
    def update_state(self, state):
        """
        description

        Args:
            state (type?): what is it?
        """
        self.state = state
        self.page2.progresstotal.config(value=state)
        if state == STARTED:
            self.page2.set_chart(self.page2.DEFAULT_CHART)
            self.page2.matcher.config(state='disabled')
            self.page2.trimbounds.config(state='disabled')
            self.page2.resetbounds.config(state='disabled')
            self.page2.mesher.config(state='disabled')
            self.page2.previewcloud.config(state='disabled')
            self.page2.chartview.config(state='disabled')
            self.page2.show.config(state='disabled')
        if state == PHOTOS:
            self.page2.set_chart(self.page2.DEFAULT_CHART)
            self.page2.trimbounds.config(state='disabled')
            self.page2.resetbounds.config(state='disabled')
            self.page2.mesher.config(state='disabled')
            self.page2.previewcloud.config(state='disabled')
            self.page2.chartview.config(state='disabled')
            self.page2.show.config(state='disabled')
            self.page2.matcher.config(state='active')
        if state == MATCHER:
            dense = Path(self.projdir / "dense")
            self.page2.set_chart(Path(dense/ "heat_map.png"))
            self.page2.show.config(state='disabled')
            self.page2.matcher.config(state='active')
            self.page2.previewcloud.config(state='active')
            self.page2.chartview.config(state='active')
            self.page2.resetbounds.config(state='active')
            self.page2.trimbounds.config(state='active')
            self.page2.mesher.config(state='active')
        if state == MESHER:
            dense = Path(self.projdir / "dense")
            self.page2.set_chart(Path(dense/ "heat_map.png"))
            self.page2.matcher.config(state='active')
            self.page2.chartview.config(state='active')
            self.page2.resetbounds.config(state='active')
            self.page2.trimbounds.config(state='active')
            self.page2.resetbounds.config(state='active')
            self.page2.mesher.config(state='active')
            self.page2.show.config(state='active')
        
        # TODO: Would there be any benefits to doing some progress bar management here with the progress text? CODEN
        # save to pickle after chnaging state
        try:
            path = self.imgdir.relative_to(self.projdir)
        except:
            path = self.imgdir
        with open(self.picklepath, 'wb') as file:
            pickle.dump((path,state), file)
    
    def _toggle_fullscreen(self, event=None):
        """
        description

        Args:
            e(event): what is it?
        """
        if self.fullscreen:
            self.attributes('-fullscreen', False)
            self.fullscreen = False
            return 'break'
        if not self.fullscreen:
            self.attributes('-fullscreen', True)
            self.fullscreen = True
            return 'break'
    def _end_fullscreen(self, event=None):
        """
        description

        Args:
            e (event): what is it?
        """
       
        if self.fullscreen:
            self.attributes('-fullscreen',False)
            self.fullscreen = False
    
    # opens a new window at the middle of the screen.
    def _open_middle(self, windoww, windowh):
        """
        description

        Args:
            windoww (int): width of the window
            windowh (int): height of the window
        """
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()  
        midx = (sw/2) - (windoww/2)
        midy = (sh/2) - (windowh/2)
        return (midx, midy-50)

    # Handler for app shutdown
    #   Cancel any living subprocesses
    #   Save recents and then kill tkinter
    def _shutdown(self):
        """
        description
        """
        try:
            self.recon.cancel()
        except:
            print("no active processes")
        print("exiting app")
        self.recents.save_recent() 
        self.destroy()

if __name__ == "__main__":
    app = main()
    app.protocol("WM_DELETE_WINDOW", app._shutdown)
    app.mainloop()

# TODO: Many things are labeled as handlers when really the handlers are in the 
    # GUI and the mathods here are secondary calls

# TODO: all non helper methods need docs formatted for the auto docs

# TODO: Style guidelines:
    # Method names use underscores: foo_bar()
    # variables are all lowercase one word: varname
    # Handlers are any method directly bound to a button or event
    # Helper functions are any which are never called externally from the class and start with _foo_bar() also not event halders
    # Classes are camel case: MethodName

# TODO: Software Design
    # GUI never interacts with file system, recon manager, or any other scripting classes directly
    # All classes that can be static should be
    # Methods should either return a value or update state/ perform an operation, never both
    # Classes should have as few fields as possible

# TODO: All python files should be in an scr folder
    # Outside the src folder there should be a single executeable, license, and the README

# TODO: Colmap should be in its own subfolder with its license info in a text file
# TODO: darkmap.png should be renamed to something more logical like blankmap.png
# TODO: following style the heat_map.png should be heatmap.png
# TODO: placeholder photo should have a better name bc thats not all it is