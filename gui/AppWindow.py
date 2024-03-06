from ttkbootstrap import Style 
import webbrowser as wb
from pathlib import Path
from tkinter import Frame, Menu, filedialog as fd, messagebox as mb
import scripts.RecentsManager as RecentsManager

# TODO: lots of header comments needed

class AppWindow(Frame):
    def __init__(self, parent, controller):
        """
        `AppWindow` is the class that inherits from `Tkinter.Frame`. It has subclasses 
        :ref:`PipelineGUI <pipelineGUI>` and :ref:`StartGUI <startGUI>`. It handles elements that
        remain consistent throughout the GUI, including the menu bar, the light and dark styling,
        and the functionality for opening new projects, existing projects, and recent projects.

        Args:
            parent (tkinter container): passed from :ref:`main <main>` to make the tkinter frame.
            controller (:ref:`main <main>`\*): a reference to main.
        """
        Frame.__init__(self, parent)
        self.controller = controller
        self._create_menu()

    # Setup method for top menu bar
    def _create_menu(self):
        """
        Setup method for top menu bar. It's displayed consistently through the Tk app with `File`,
        `Info`, and `Reconstruction` menus that let the user navigate through projects, access the
        docs, and run all pipeline steps automatically.
        """
        # Main menu object (the bar)
        self.menubar = Menu(self)

        # menus that make up the tabs of the menu bar, from left to right.
        self.file = Menu(self.menubar, tearoff=0)
        styles = Menu(self.file, tearoff=0)
        self.recent = Menu(self.file, tearoff=0, postcommand=lambda: self._recent_menu()) # postcommand creates recents cascade.
        info = Menu(self.menubar, tearoff=0)
        recon = Menu(self.menubar, tearoff=0)

        ## File menu (first tab)
        self.file.add_command(label="Back to Start", command=lambda: self.controller.back_to_start())
        self.file.add_command(label="New", command=lambda: self.new_project())  
        self.file.add_command(label="Open", command=lambda: self.open_project())  
        self.file.add_separator()  
        # style is cascade, only appears on hover as an offshoot of "Set Style..."
        self.file.add_cascade(label="Set Style...", menu=styles)
        styles.add_command(label="Dark", command=lambda: self._start_darkmode())
        styles.add_command(label="Light", command=lambda: self._start_lightmode()) 
        self.file.add_separator()
        # recent is also cascade, only appears on hover as an offshoot of "Open Recent..."
        self.file.add_cascade(label="Open Recent...", menu=self.recent)
         

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
        Helper method that creates the menu cascade under "Open Recents..." in the file menu.
        It refreshes the menu elements displayed when the menu is opened, with open file at the top
        and the least recently opened file at the bottom. The menu can display 0 to 4 projects.

        As it can be called repeatedly, the method starts by removing all elements from the cascade
        before adding new ones. It uses `get()` from :ref:`RecentsManager <recentsmanager>` to use
        up-to-date recent values.
        """
        self.recent.delete(0, "end")
        recentstack = RecentsManager.get()
        numrecents = len(recentstack)
        if numrecents == 0:
            self.recent.add_command(label="no recents found")
        if numrecents >= 1:
            self.recent.add_command(label=str(Path(recentstack[-1]).stem), command=lambda: self.open_recent(Path(recentstack[-1])))
        if numrecents >= 2:
            self.recent.add_command(label="1 " + str(Path(recentstack[-2]).stem), command=lambda: self.open_recent(Path(recentstack[-2])))
        if numrecents >= 3:
            self.recent.add_command(label="2 " + str(Path(recentstack[-3]).stem), command=lambda: self.open_recent(Path(recentstack[-3])))
        if numrecents >= 4:
            self.recent.add_command(label="3 " + str(Path(recentstack[-4]).stem), command=lambda: self.open_recent(Path(recentstack[-4])))


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
        Event handler for opening existing projects. It handles the "Open" menu item and the items
        under the "Open Recent..." cascade in the `File` menu tab, and the "Open Project" button on
        the start screen of the Tk app. If a project file directory is passed or the user selects a
        file directory using the dialog, then the function calls the controller's `open_project`
        method in :ref:`main <main>` with the project file directory.

        Args:
            projfile (pathlib.Path): optional path to a .vrp file
        """
        if not projfile:
            projfile = fd.askopenfilename(filetypes=[('Choose a project (.vrp) file', '*.vrp')])
            if not projfile:
                return
        self.controller.open_project(Path(projfile))
        
    def open_recent(self,recent):
        """
        Event handler for the menu items representing files in the recents dictionary under the 
        "Open Recents..." cascade in the `File` menu tab in the menu bar. If the project exists,
        then it's passed to `open_project()`.

        Args:
            recent (pathlib.Path): a string of the path of the recent file to open
        """
        try:
            print("opening recent: " + str(recent))
            if not recent:
                return
            self.open_project(recent)
        except Exception as e:
            print(e)
            print("Could not find project")

    # Handler for setting dark mode
    #   changes theme to a dark theme
    #   might be worth adding some flag so that we don't have to switch if we already have one style.
    def _start_darkmode(self):
        """
        Handler for setting the app to dark mode.
        Uses `ttkbootstrap <https://ttkbootstrap.readthedocs.io/en/latest/themes/>`_ theme 
        `"darkly"`. If the app isn't already in dark mode, it changes the style and sets
        :ref:`main <main>`'s `styleflag`.
        """
        if (self.controller.styleflag == "dark"):
            return
        self.controller.style = Style("darkly")
        self.controller.styleflag = "dark"
        self.controller.init_style()

    def _start_lightmode(self):
        """
        Handler for setting the app to light mode.
        Uses `ttkbootstrap <https://ttkbootstrap.readthedocs.io/en/latest/themes/>`_ theme 
        `"lumen"`. If the app isn't already in light mode, it changes the style and sets
        :ref:`main <main>`'s `styleflag`.
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
        Handler for all of the menu elements under the info menu on the menu bar. Opens different
        pages of the **VirtualRocks** documentation depending on what `docpage` is passed.

        Args:
            docpage (string): the name of the documentation page to open. Defaults to the main page, `index.html`.
        """
        try:
            wb.open_new('file:///' + str(Path(f"docs/_build/html").absolute().as_posix()) + "/" + docpage)
        except Exception as e:
            print(e)
        return
    