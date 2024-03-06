import os
import shutil
import subprocess
import sys
from ttkbootstrap import Style
from tkinter import simpledialog, PhotoImage, Frame, Tk
from pathlib import Path
from threading import Thread
import scripts.PhotoManager as pm
from gui.PipelineGUI import PipelineGUI
from gui.StartGUI import StartGUI
from scripts.ReconManger import ReconManager
import pickle
import ctypes
import scripts.PointCloudManager as PointCloudManager
import scripts.RecentsManager as RecentsManager

# Compiler run: pyinstaller --onefile main.py -w -p "scripts" -p "gui" -c
# After compiles move main.exe into the VirtualRocks directory

# DEBUG = True will cause the application to skip over recon scripts for testing
DEBUG = False

# Progress Constants
STARTED = 0
PHOTOS = 10
MATCHER = 70
MESHER = 100

# Path to specific python version installed by the installer
PYTHONPATH = os.getenv('LOCALAPPDATA') + "\\Programs\\Python\\Python311\\python.exe"

class main(Tk):

    def __init__(self, *args, **kwargs):
        """
        general class desc, args.
        """
        Tk.__init__(self, *args, **kwargs)

        # Controller Variables
        self.projdir = None
        self.imgdir = ""
        self.recon = None
        self.state = STARTED
        self.fullscreen = False

        # Sets app icon and identifier
        self.myappid = u'o7.VirtualRocks.PipelineApp.version-1.0' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(self.myappid)
        
        # Configuration variables
        self.projectname = "project"
        self.picklepath = None
        self.minsize(500, 300)
        centerdim = self._open_middle(1000,700)
        self.geometry('%dx%d+%d+%d' % (1000, 700, centerdim[0], centerdim[1]))
        self.title("VirtualRocks")
        icon = PhotoImage(file=Path(r"gui\placeholder\logo.png").resolve())
        self.iconphoto(True, icon)

        # Application styling
        self.style = Style("darkly")
        self.styleflag = "dark"
        self.init_style()

        # container is a stack of frames (aka our two main pages)
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        if not args[0]:
            # Load staring page and start application
            self.page1 = StartGUI(parent=self.container, controller=self)
            self.page1.grid(row=0, column=0, sticky="nsew")
            self.page1.tkraise()
        else:
            # Open project directly
            self.open_project(args[0])

        # Binding for fullscreen toggle
        self.bind("<F11>", self._toggle_fullscreen)
        self.bind("<Escape>", self._end_fullscreen)

    # Common startup tasks for both opening and creating projects
    def _startup(self):
        """
        description
        """
        self.page2 = PipelineGUI(self.container, self, self.projdir)
        self.page2.grid(row=0, column=0, sticky="nsew")
        self.page2.set_example_image(self.page2.DEFAULT_PREVIEW)
        self.page2.tkraise()
        self.recon = ReconManager(self, self.projdir)
        self.page2.menubar.entryconfig("Reconstruction", state="normal")
        RecentsManager.add(self.picklepath)

    def init_style(self):
        """
        Handles assignment of style elements when app starts or when the style changes. This 
        includes the button size, the title font size on the start page, and progress bar
        appearance. The progress on the current step, if one is running, is also reprinted to the
        bar.
        """
        # setting initial style stuff
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
        #need to add the progress bar update stuff here.
        currentprogress = self._get_progress()
        if 0 < currentprogress < 100: 
            self.style.configure('prog.Horizontal.TProgressbar', text='{:g} %'.format(currentprogress))


    # Handler for creating of a new project
    #   Create a PipelineGUI object and load it onto the application
    def new_project(self, projdir, name=None, imgdir=None):
        """
        Handler method for creating a new project.

        Args:
            projdir (pathlib.Path): project directory to save .pkl file in.
            name (str): optional, the name of the project.
            imgdir (pathlib.Path): optional, image directory

        .. warning::
            this, and anything with blank desc, needs to be finished.
        """
        print("creating new project")
        self.projdir = Path(projdir)
        if not name:
            self.projectname = simpledialog.askstring(title="Name Project As...", prompt="Enter a name for this project:", parent=self.page1, initialvalue=self.projectname)
        else:
            self.projectname = name
        self.picklepath = self.projdir / Path(self.projectname + '.vrp')
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
            projdir (pathlib.Path): Project directory containing .pkl file.
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
        Handler method for reopening the starting page when the "Back to Start" menu item in the
        `File` menu tab in :ref:`AppWindow <appwindow>` is pressed. It reopens the Tk Frame made by
        :ref:`StartGUI <startGUI>`, resets the app title, and disables the `Reconstruction` menu
        tab.
        """
        self.page1.tkraise()
        self.page2.menubar.entryconfig("Reconstruction", state="disabled")
        self.title("VirtualRocks")

    # Handler for adding photos
    #   Set the controller variable for image directory
    #   This method should not open a dialogue, the is the role of the GUI classes
    def add_photos(self, imgdir):
        """
        Method that sets the controller variable for image directory and sets the example image
        from pictures in the selected image directory. Progress on this step is tracked using the
        `_send_log()` helper function in :ref:`ReconManager <reconmanager>`.

        The handler method `photos_handler()` in :ref:`PipelineGUI <pipelineGUI>` opens a dialog
        that allows the user to select an image directory.

        Args:
            imgdir (pathlib.Path): path to the image directory
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
    def set_bounds(self, minx, maxx, miny, maxy, minz, maxz):
        """
        Method communicates between the GUI and the PointCloudManager for trimming models by
        removing points from the dense point clouds.
        This step automatically completes, and its progress is tracked using the `_send_log()`
        helper function in :ref:`ReconManager <reconmanager>`.
        The handler method `bounds_handler()` in :ref:`PipelineGUI <pipelineGUI>` creates the dialog
        (using the :ref:`BoundsDialog <boundsdialog>` class) and passes the bounds received from
        the user to this method.

        Args:
            minx (float): minimum x axis bound
            maxx (float): maximum x axis bound
            miny (float): minimum y axis bound
            maxy (float): maximum y axis bound
            minz (float): minimum z axis bound
            maxz (float): maximum z axis bound

        .. warning::    
            are the bounds inclusive or exclusive? change in pointcloudmanager too.
        """
        self.recon._send_log("$$")
        self.recon._send_log("$Trimming Bounds..100$")
        dense = Path(self.projdir / "dense")
        PointCloudManager.remove_points(Path(dense / "fused.ply"), minx, maxx, miny, maxy, minz, maxz)
        self.page2.log("Trimming complete")
        PointCloudManager.create_heat_map(Path(dense / "fused.ply"), dense)
        self.page2.set_chart(Path(dense/ "heat_map.png"))

    # Handler for the restore point cloud menu item
    #   Should overwrite the current fused.ply with the un-edited save.ply
    #   Serves to undo the set bounds
    def restore(self):
        """
        Handler method for the "Reset" button on the setting bounds step in 
        :ref:`PipelineGUI <pipelineGUI>`. It overwrites the current `fused.ply` file with the 
        unedited `save.ply` copy. The method undoes any previous point cloud trims done when
        setting bounds.
        """
        if self.state >= MATCHER:
            self.page2.log("Point cloud restoration complete")
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
        Handler method for starting the mesher (:ref:`Colmap <colmap>`), called via "2: Matcher"
        button press in :ref:`PipelineGUI <pipelineGUI>`.

        It starts a new thread for the `matcher()` method in the :ref:`ReconManager <reconmanager>`
        class.
        """
        self.recon.imgdir = self.imgdir
        self.thread1 = Thread(target = self.recon.matcher)
        self.thread1.daemon = True
        self.thread1.start()

    # Handler for starting mesher
    #   Starts a new thread for the ReconManager.mesher() method
    def start_mesher(self):
        """
        Handler method for starting the mesher (:ref:`pymeshlab <meshlab>`), called via "3: Mesher"
        button push in :ref:`PipelineGUI <pipelineGUI>`.

        It starts a new thread for the `mesher()` method in the :ref:`ReconManager <reconmanager>`
        class.
        """
        self.recon.imgdir = self.imgdir
        self.thread1 = Thread(target = self.recon.mesher)
        self.thread1.daemon = True
        self.thread1.start()

    # Handler for the automatic reconstruction feature
    #   Starts a new thread for the ReconManager.auto() method
    def auto_recon(self):
        """
        Handler method for the automatic reconstuction feature, called by a command in the 
        `Reconstruction` file menu in :ref:`AppWindow <appwindow>`. 
        
        It starts a new thread for the `auto()` method in the :ref:`ReconManager <reconmanager>`
        class.

        .. warning::  
            Using :ref:`ReconManager <reconmanager>`'s `auto()` method does not allow the user to
            trim the point cloud. It's useful when running the app on a large dataset or overnight,
            but will likely result in a final mesh that includes outlier points.
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
        Handler method for cancelling the reconstruction, no matter the step it's on. It's called
        by the "Cancel" button :ref:`PipelineGUI <pipelineGUI>`, and when changing project 
        directory with :ref:`PipelineGUI <pipelineGUI>`'s `change_projdir()`.
        """
        self.recon.cancel()

    def preview_cloud(self):
        """
        Handler method for the "Preview Point Cloud" button beneath the chart in
        :ref:`PipelineGUI <pipelineGUI>`. It starts a subprocess to open an ``open3d`` viewer
        window of the current project file, which will remain open even if the **VirtualRocks**
        window is closed.
        """
        path = Path(self.projdir / 'dense' / 'fused.ply')
        p = subprocess.Popen([PYTHONPATH, 'scripts/CloudPreviewer.py', str(path)])

    # Method for updating the state of the application
    #   Should set the map image accordingly as well as activate and deactivate buttons
    def update_state(self, state):
        """
        Method for updating the state of the application, which controls which buttons are 
        activated and the image the chart is set to. The method also controls the value of the
        total progress bar. Called when opening projects and progressing through the pipeline to
        gradually enable functionality when applicable.

        Args:
            state (type?): what is it?

        .. warning::
            what type is the state?
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

        .. warning::
            So like, what is an event? Is this going to be a specific event or is it just any... We
            need to fix this in some other places too, so use the search bar to find all mentions
            of 'event'.
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
    
    def _get_progress(self):
        """
        description

        Returns:
            int: percentage of progress made on the current step.
        """
        if self.recon:
            return self.recon.progresspercent
        else:
            return -1

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
        self.destroy()

if __name__ == "__main__":
    pklfile = None
    try:
        pklfile = sys.argv[1]
        print(pklfile)
    except:
        pass
    app = main(pklfile)
    app.protocol("WM_DELETE_WINDOW", app._shutdown)
    app.mainloop()