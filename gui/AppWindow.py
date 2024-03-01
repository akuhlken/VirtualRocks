from ttkbootstrap import Style 
import webbrowser as wb
from pathlib import Path
from tkinter import Frame, Menu, filedialog as fd, messagebox as mb

# TODO: lots of header comments needed

class AppWindow(Frame):
    def __init__(self, parent, controller, recents):
        """
        description of the class as a whole.

        Args:
            parent (type?): what is it?
            controller (type?): what is it?
            recents (type?): what is it?
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
        file = Menu(self.menubar, tearoff=0)  
        styles = Menu(file, tearoff=0)
        self.recent = Menu(file, tearoff=0, postcommand=self.recents.update_recent(pklpath=self.controller.picklepath))
        info = Menu(self.menubar, tearoff=0)
        recon = Menu(self.menubar, tearoff=0)

        ## File menu (first tab)
        file.add_command(label="Back to Start", command=lambda: self.controller.back_to_start())
        file.add_command(label="New", command=lambda: self.new_project())  
        file.add_command(label="Open", command=lambda: self.open_project())
        file.add_command(label="Save")  
        file.add_command(label="Save as")    
        file.add_separator()  
        # style is cascade, only appears on hover as an offshoot of "Set Style..."
        file.add_cascade(label="Set Style...", menu=styles)
        styles.add_command(label="Dark", command=lambda: self._start_darkmode())
        styles.add_command(label="Light", command=lambda: self._start_lightmode()) 
        file.add_separator()
        # recent is also cascade, only appears on hover as an offshoot of "Open Recent..."
        file.add_cascade(label="Open Recent...", menu=self.recent)
        # the number of recent files/menu items displayed depends on how many exist.
        self._menu_recents()

        # Info menu, access to the docs.
        info.add_command(label="Common Issues", command=lambda: self.open_helpmenu()) 
        info.add_command(label="Colmap Info", command=lambda: self.open_helpmenu("colmap.html")) 
        info.add_command(label="MeshLab Info", command=lambda: self.open_helpmenu("meshlab.html"))

        # Recon menu
        recon.add_command(label="Auto Reconstruction", command=lambda: self.controller.auto_recon())

        # Add menues to the menu bar as cascades
        self.menubar.add_cascade(label="File", menu=file)
        self.menubar.add_cascade(label="Info", menu=info) 
        self.menubar.add_cascade(label="Reconstruction", menu=recon) 
        self.controller.config(menu=self.menubar)
        self.menubar.entryconfig("Reconstruction", state="disabled")


    def _menu_recents(self):
        """
        Helper method to display the correct number of recent files in the recent cascade menu.
        Since the number of filepaths saved in the dictionary of recent values can be anywhere from
        0 to 4, the number of menu items should match the number of existing recent files. If there
        aren't any, then there are no clickable menu items displayed under the recent menu.
        """
        numrecents = len(self.recents.recentdict)
        if numrecents == 0:
            self.recent.add_command(label="no recents found")
        for x in range(numrecents):
            recentlabel = str(x) + " " + str(Path(self.recents.recentdict[-x][0]).stem)
            self.recent.add_command(label=recentlabel, command=lambda: self.open_recent(x))

    # Event handler for the "new project" menu item
        # Should open a dialogue asking the user to selct a working directory
        # Then call controllers new_project method
    def new_project(self):
        """
        description
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
        description

        Args:
            projfile (type?): what is it?
        """
        if not projfile:
            projfile = fd.askopenfilename(filetypes=[('Choose a project (.pkl) file', '*.pkl')])
            if not projfile:
                return
        self.controller.open_project(Path(projfile))
        
    def open_recent(self,index=1):
        """
        description

        Args:
            index (int): index of recent file to open in the recents dictionary.
        """
        index = -index
        try:
            projfile = self.recents.recentdict[index][0]
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
        description. Uses Ttkbootstrap theme `"darkly"`.
        """
        if (self.controller.styleflag == "dark"):
            return
        self.controller.style = Style("darkly")
        self.controller.styleflag = "dark"
        self.controller.init_style()

    def _start_lightmode(self):
        """
        description. Uses Ttkbootstrap theme `"darkly"`.
        """
        if (self.controller.styleflag == "light"):
            return
        self.controller.style = Style("lumen")
        self.controller.styleflag = "light"
        self.controller.init_style()

    # Handler for opening the help menu/docs
    #   can take argument to specify which page to open if it isn't the main page.
    def open_helpmenu(self, docpage = "index.html"):
        """
        description
        """
        try:
            wb.open_new(('file:///' + str(Path(f"docs/_build/html").absolute()) + "/" + docpage).replace("\\","/"))
        except Exception as e:
            print(e)
        return