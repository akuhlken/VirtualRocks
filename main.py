from ttkbootstrap import Style
from tkinter import simpledialog, PhotoImage, Frame, Tk
from pathlib import Path
from threading import Thread
from scripts.PhotoManager import PhotoManager
from gui.PipelineGUI import PipelineGUI
from gui.StartGUI import StartGUI
from scripts.ReconManger import ReconManager
import pickle
import ctypes   # for adding icon to taskbar
import json
import scripts.PointCloudManager as pcm

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
        self.image = None
        self.recon = None
        self.state = STARTED
        self.recentlist = list()      # saved to JSON file as a dict, but needs to be list (of tuples) to be usable.
        self.numrecents = 0
        self.get_recent()

        # for loading icon on taskbar, basically just says we aren't doing only python.
        self.myappid = u'o7.VirtualRocks.PipelineApp.version-1.0' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(self.myappid)
        
        # Configuration variables
        self.projectname = "project"
        self.picklepath = ""
        self.minsize(500, 300)
        centerdim = self.open_middle(1000,700)
        self.geometry('%dx%d+%d+%d' % (1000, 700, centerdim[0], centerdim[1]))
        self.title("VirtualRocks")
        icon = PhotoImage(file=Path(r"gui\placeholder\logo.png").resolve())
        self.iconphoto(True, icon)

        # Importing external styles
        Style.load_user_themes = Path(f"gui/goblinmode.py").resolve()

        # Application styling
        self.buttoncolor = "#ffffff"  # for the buttons on page 1
        self.logbackground = "#ffffff"
        self.style = Style("darkly")
        self.styleflag = "dark"

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
        self.page1 = StartGUI(parent=self.container, controller=self)
        self.page1.grid(row=0, column=0, sticky="nsew")
        self.page1.tkraise()

        #toggling fullscreen and escaping
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)

    #key binding 
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen  # Just toggling the boolean
        self.attributes("-fullscreen", self.fullscreen)
        return "break"

    def end_fullscreen(self, event=None):
        self.fullscreen = False
        self.attributes("-fullscreen", False)
        return "break"

    # Common startup tasks for both opening and creating projects
    def _startup(self):
        self.page2 = PipelineGUI(self.container, self, self.projdir)
        self.page2.grid(row=0, column=0, sticky="nsew")
        self.page2.set_example_image(self.page2.DEFAULT_PREVIEW)
        self.page2.tkraise()
        self.recon = ReconManager(self, self.projdir)
        self.page2.menubar.entryconfig("Reconstruction", state="normal")

    # Handler for creating of a new project
    #   Create a PipelineGUI object and load it onto the application
    def new_project(self, projdir, name=None, imgdir=None):
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
            pm = PhotoManager(self.imgdir)
            self.page2.update_text(pm.numimg)
            self.page2.set_example_image(self.imgdir / Path(pm.get_example()))
            self._update_state(PHOTOS)
        else:
            self._update_state(STARTED)
        
    # Handler for loading an existing project
    #   Method should read a project save file and create a PipelineGUI object
    def open_project(self, projfile):
        print("opening project")
        self.picklepath = projfile
        self.projectname = Path(projfile).stem
        # Load the path variables from the file
        #print(projfile)
        self.projdir = Path(projfile).parent
        with open(projfile, 'rb') as file:
            (path,self.state) = pickle.load(file)
        if Path(path).is_absolute():
            self.imgdir = path
        else:
            self.imgdir = self.projdir / path
        self._startup()
        self._update_state(self.state)
        self.title("VirtualRocks: " + self.projectname)

        #print("in update: " + str(self.picklepath))

        self.update_recent()
        self.page2.dirtext.config(text=f"Workspace: [ {self.projdir} ]")
        try:
            pm = PhotoManager(self.imgdir)
            self.page2.update_text(pm.numimg)
            self.page2.set_example_image(self.imgdir / Path(pm.get_example()))
        except Exception as e:
            self.recon._send_log("Could not find image directory")
            self._update_state(STARTED)
            print(e)


    # opens a new window at the middle of the screen.
    def open_middle(self, windoww, windowh):
        sw = self.winfo_screenwidth()    # screen width
        sh = self.winfo_screenheight()   # screen height
        midx = (sw/2) - (windoww/2)                # middle x based on size of window
        midy = (sh/2) - (windowh/2)                # middle y based on size of window
        return (midx, midy-50)                        # return the new coordinates for the middle


    # Handler for reopening the starting page
    #   since there's an option for it in the menu, it must be done.
    def start_menu(self):
        self.page1.tkraise()
        self.page2.menubar.entryconfig("Reconstruction", state="disabled")
        self.title("VirtualRocks")

    # Saving value of progress to make progress bar after style update accurate.
    #   used by AppWindow.py.
    def swtich_style(self):
        if self.recon:
            return self.recon.progresspercent
        else:
            return -1

    # Handler for adding photos
    #   Set the controller variable for image directory
    #   This method should not open a dialogue, the is the role of the GUI classes
    def add_photos(self, imgdir):
        self.recon._send_log("$$")
        self.recon._send_log("$.Image Loading.0$")
        self.projdir.resolve()
        self.imgdir = Path(imgdir).resolve()
        pm = PhotoManager(self.imgdir)
        self.recon._send_log("$Image Loading..100$")
        self.page2.update_text(pm.numimg)
        self.page2.set_example_image(self.imgdir / Path(pm.get_example()))
        self._update_state(PHOTOS)
            
        # updates the .txt doc that tracks recent values. b/c this is where we make .pkl files,
        # this one tracks new files.
        self.update_recent()

    # Handler for seeting the project bounds
    #   Set the controller variables acording to bounds specified by the user
    #   This method should not open a dialogue, the is the role of the GUI classes
    def set_bounds(self, minx, maxx, miny, maxy):      
        self.recon._send_log("$$")
        self.recon._send_log("$Setting Bounds..100$")
        dense = Path(self.projdir / "dense")
        pcm.remove_points(Path(dense / "fused.ply"), minx, maxx, miny, maxy)
        pcm.create_heat_map(Path(dense / "fused.ply"), dense)
        self.page2.set_map(Path(dense/ "heat_map.png"))

    # Handler for starting recon
    #   Start a new thread with the _recon() method
    def start_matcher(self):
        self.recon.imgdir = self.imgdir
        self.thread1 = Thread(target = self.recon.matcher)
        self.thread1.daemon = True
        self.thread1.start()

    # Handler for starting recon
    #   Start a new thread with the _recon() method
    def start_mesher(self):
        self.recon.imgdir = self.imgdir
        self.thread1 = Thread(target = self.recon.mesher)
        self.thread1.daemon = True
        self.thread1.start()

    # Handler for canceling recon
    #   Should kill any active subprocess as well as set the kill flag in dense2mesh.py
    #   After cancel it should change the action button back to start
    def cancel_recon(self):
        self.recon.cancel()

    # Handler for the automatic reconstruction feature
    def auto_recon(self):
        if not self.imgdir:
            self.recon._send_log("No images loaded")
            return
        self.recon.imgdir = self.imgdir
        self.thread1 = Thread(target = self.recon.auto)
        self.thread1.daemon = True
        self.thread1.start()

    def update_recent(self):
        # used by menu to update, basically the menu is refreshed every time this is called (needs to handle blanks)
        # if picklepath is null, then we shouldn't add anything to the dict.
        #   the values should add. get the max current and add one?
        #   basically, we don't need a dictionary for function, but we want to use JSON so we need it
        #   should also have something that limits the length of recent to 4 so we don't save more things to loop thru.
        strpickle = str(Path(self.picklepath).as_posix())
    
        while len(self.recentlist) > 4:
            #print("removing " + str(self.recentlist[0]) + " from recents")
            del self.recentlist[0]
        for rectup in self.recentlist:
            if strpickle == rectup[0]:
                self.recentlist.remove(rectup)
        if self.picklepath:     # if there is a picklepath (there should also be an image path)
            self.recentlist.append((strpickle, self.numrecents))
            self.numrecents += 1

    def save_recent(self):
        with open(Path("main.py").parent / 'recents.json', 'w') as f:
            json.dump(self.recentlist, f)
            print("saved recent files.")
    

    def get_recent(self):
        with open(Path("main.py").parent / 'recents.json') as f:
            # need to check if empty
            recentdict = json.load(f)
            self.recentlist = list(dict(recentdict).items())
            #print(self.recentlist)

    def _update_state(self, state):
        self.state = state
        self.page2.progresstotal.config(value=state)
        if state == STARTED:
            self.page2.set_map(self.page2.DEFAULT_MAP)
            self.page2.matcher.config(state='disabled')
            self.page2.setbounds.config(state='disabled')
            self.page2.mesher.config(state='disabled')
            self.page2.show.config(state='disabled')
        if state == PHOTOS:
            self.page2.set_map(self.page2.DEFAULT_MAP)
            self.page2.setbounds.config(state='disabled')
            self.page2.mesher.config(state='disabled')
            self.page2.show.config(state='disabled')
            self.page2.matcher.config(state='active')
        if state == MATCHER:
            dense = Path(self.projdir / "dense")
            self.page2.set_map(Path(dense/ "heat_map.png"))
            self.page2.show.config(state='disabled')
            self.page2.matcher.config(state='active')
            self.page2.setbounds.config(state='active')
            self.page2.mesher.config(state='active')
        if state == MESHER:
            dense = Path(self.projdir / "dense")
            self.page2.set_map(Path(dense/ "heat_map.png"))
            self.page2.matcher.config(state='active')
            self.page2.setbounds.config(state='active')
            self.page2.mesher.config(state='active')
            self.page2.show.config(state='active')

        # save to pickle
        try:
            path = self.imgdir.relative_to(self.projdir)
        except:
            path = self.imgdir
        with open(self.picklepath, 'wb') as file:
            pickle.dump((path,state), file)

    def _shutdown(self):
        try:
            self.recon.cancel()
        except:
            print("no active processes")
        print("exiting app")
        self.save_recent()                  # save recents at the very end
        self.destroy()

if __name__ == "__main__":
    app = main()
    app.protocol("WM_DELETE_WINDOW", app._shutdown)
    app.mainloop()
