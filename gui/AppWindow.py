from ttkbootstrap import Style 
import webbrowser as wb
from pathlib import Path
from tkinter import Frame, Menu, filedialog as fd, messagebox as mb

# TODO: lots of header comments needed

class AppWindow(Frame):
    def __init__(self, parent, controller, recents):
        """
        `AppWindow` is the parent class.

        Args:
            parent (tkinter container): passed from :ref:`main <main>` to make the tkinter frame.
            controller (:ref:`main <main>`\*): a reference to main.
            recents (:ref:`recents <recentsmanager>` object): a RecentsManager object that stores and maintains the dictionary of recent projects.
        """
        Frame.__init__(self, parent)
        self.controller = controller
        self.recents = recents
        self._create_menu()

    # Setup method for top menu bar
    def _create_menu(self):
        """
        description
        """
        # Main menu object (the bar)
        self.menubar = Menu(self)

        # menus that make up the tabs of the menu bar, from left to right.
        self.file = Menu(self.menubar, tearoff=0)  
        styles = Menu(self.file, tearoff=0)
        self.recent = Menu(self.file, tearoff=0)
        info = Menu(self.menubar, tearoff=0)
        recon = Menu(self.menubar, tearoff=0)

        ## File menu (first tab)
        self.file.add_command(label="Back to Start", command=lambda: self.controller.back_to_start())
        self.file.add_command(label="New", command=lambda: self.new_project())  
        self.file.add_command(label="Open", command=lambda: self.open_project())
        self.file.add_command(label="Save")  
        self.file.add_command(label="Save as")    
        self.file.add_separator()  
        # style is cascade, only appears on hover as an offshoot of "Set Style..."
        self.file.add_cascade(label="Set Style...", menu=styles)
        styles.add_command(label="Dark", command=lambda: self._start_darkmode())
        styles.add_command(label="Light", command=lambda: self._start_lightmode()) 
        self.file.add_separator()
        # recent is also cascade, only appears on hover as an offshoot of "Open Recent..."
        #file.add_cascade(label="Open Recent...", menu=self.recent)
        # the number of recent files/menu items displayed depends on how many exist.
        #self._recent_menu()
        self.file.add_cascade(label="Open Recent...", menu=self.recent, postcommand=self.recents.update_recent(pklpath=self.controller.picklepath))

        self.recent.add_command(label="print recents", command=lambda: print(self.recents.recentdict))
        numrecents = len(self.recents.recentdict)
        if numrecents == 0:
            self.recent.add_command(label="no recents found")
        for x in range(numrecents):
            if x == 0:
                self.recent.add_command(label=str(Path(self.recents.recentdict[0][0]).stem), command=lambda: self.open_recent(0))
            else:
                recentlabel = str(x) + " " + str(Path(self.recents.recentdict[-x][0]).stem)
                self.recent.add_command(label=recentlabel, command=lambda: self.open_recent(-x))

        # Info menu, access to the docs.
        info.add_command(label="FAQ", command=lambda: self._open_helpmenu("FAQ.html")) 
        info.add_command(label="Reference", command=lambda: self._open_helpmenu("reference/references.html"))
        info.add_command(label="Unity", command=lambda: self._open_helpmenu("unity.html"))

        # Recon menu
        recon.add_command(label="Auto Reconstruction", command=lambda: self.controller.auto_recon())

        # Add menues to the menu bar as cascades
        self.menubar.add_cascade(label="File", menu=self.file)
        self.menubar.add_cascade(label="Info", menu=info) 
        self.menubar.add_cascade(label="Reconstruction", menu=recon) 
        self.controller.config(menu=self.menubar)
        self.menubar.entryconfig("Reconstruction", state="disabled")


    def _recent_menu(self):
        """
        Helper method to display the correct number of recent files in the recent cascade menu.
        There can be between 0 and 4 recent files at one time, so the number of menu items 
        should match the number of existing recent files. If there aren't any, then there are no
        clickable menu items displayed under the recent menu.
        """
        self.file.add_cascade(label="Open Recent...", menu=self.recent, postcommand=self.recents.update_recent(pklpath=self.controller.picklepath))

        self.recent.add_command(label="print recents", command=lambda: print(self.recents.recentdict))
        numrecents = len(self.recents.recentdict)
        if numrecents == 0:
            self.recent.add_command(label="no recents found")
        for x in range(numrecents):
            if x == 0:
                recentlabel = str(Path(self.recents.recentdict[0][0]).stem)
                self.recent.add_command(label=recentlabel, command=lambda: self.open_recent(0))
            else:
                recentlabel = str(x) + " " + str(Path(self.recents.recentdict[-x][0]).stem)
                self.recent.add_command(label=recentlabel, command=lambda: self.open_recent(-x))

    # Event handler for the "new project" menu item
        # Should open a dialogue asking the user to selct a working directory
        # Then call controllers new_project method
    def new_project(self):
        """
        Event handler for opening new projects. It handles the "New" menu item under then `File`
        menu tab and the "New Project" button on the start screen on the Tk app. It opens a dialog
        that prompts the user to select a workspace/working directory. Once the user selects a
        valid directory, it calls the controller's `new_project` method in :ref:`main <main>`.
        """
        projdir = fd.askdirectory(title='Select Workspace', initialdir='/home/')
        if not projdir:
            return
        if ' ' in projdir:
            print("Path must not contain white spaces")
            mb.showerror("Paths cannot contain whitespace                           ")
            return
        self.controller.new_project(projdir)

    # Event handler for the "open project" menu item
        # Should open a dialogue asking the user to selct a project file
        # Then call controllers open_project method
    def open_project(self, projfile=None):
        """
        Event handler for opening existing projects. It handles the "Open" menu item and the files
        under the "Open Recent..." cascade in the `File` menu tab, and the "Open Project" button on
        the start screen of the Tk app. If a project file directory is passed to the function or
        the user selects a file directory using the dialog, then the function calls the 
        controller's `open_project` method in :ref:`main <main>` with the project file directory.

        Args:
            projfile (pathlib.Path): optional path to a .pkl file
        """
        if not projfile:
            projfile = fd.askopenfilename(filetypes=[('Choose a project (.pkl) file', '*.pkl')])
            if not projfile:
                return
        self.controller.open_project(Path(projfile))
        
    def open_recent(self,index=-1):
        """
        Event handler for the menu items representing files in the recents dictionary under the 
        "Open Recents..." cascade in the `File` menu tab in the menu bar.

        Args:
            index (int): index of recent file to open in the recents dictionary.
        """
        try:
            projfile = self.recents.recentdict[index][0]
            print(self.recents.recentdict[index][0])
            if not projfile:
                return
            self.open_project(projfile)
        except Exception as e:
            print(e)
            print("Could not find project")

    # Handler for setting dark mode
    #   changes theme to a dark theme
    #   might be worth adding some flag so that we don't have to switch if we already have one style.
    def _start_darkmode(self):
        """
        description. Uses `ttkbootstrap <https://ttkbootstrap.readthedocs.io/en/latest/themes/>`_
        theme `"darkly"`.
        """
        if (self.controller.styleflag == "dark"):
            return
        self.controller.style = Style("darkly")
        self.controller.styleflag = "dark"
        self.controller.init_style()

    def _start_lightmode(self):
        """
        description. Uses `ttkbootstrap <https://ttkbootstrap.readthedocs.io/en/latest/themes/>`_
        theme `"lumen"`.
        """
        if (self.controller.styleflag == "light"):
            return
        self.controller.style = Style("lumen")
        self.controller.styleflag = "light"
        self.controller.init_style()

    # Handler for opening the help menu/docs
    #   can take argument to specify which page to open if it isn't the main page.
    def _open_helpmenu(self, docpage = "index.html"):
        """
        Handler for all of the buttons under the info menu on the menu bar. Opens different pages
        of **VirtualRocks** documentation depending on what value is passed as the `docpage`.

        Args:
            docpage (string): the name of the documentation page to open. Defaults to the main page, `index.html`.
        """
        try:
            wb.open_new('file:///' + str(Path(f"docs/_build/html").absolute().as_posix()) + "/" + docpage)
        except Exception as e:
            print(e)
        return