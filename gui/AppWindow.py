from ttkbootstrap import Style 
import webbrowser as wb
from pathlib import Path
from tkinter import Frame, Menu, filedialog as fd, messagebox as mb
from scripts.RecentsManager import RecentsManager

# TODO: lots of header comments needed

class AppWindow(Frame):
    def __init__(self, parent, controller, recents):
        Frame.__init__(self, parent)
        self.controller = controller
        self.recents = recents
        self.create_menu()

    # Setup method for top menu bar
    def create_menu(self):
        self.menubar = Menu(self)
        file = Menu(self.menubar, tearoff=0)  
        file.add_command(label="Back to Start", command=lambda: self.controller.start_menu())
        file.add_command(label="New", command=lambda: self.new_project())  
        file.add_command(label="Open", command=lambda: self.open_project())
        file.add_command(label="Save")  
        file.add_command(label="Save as")    
        file.add_separator()  
 
        styles = Menu(file, tearoff=0)
        file.add_cascade(label="Set Style...", menu=styles)
        styles.add_command(label="Dark", command=lambda: self.start_darkmode())
        styles.add_command(label="Light", command=lambda: self.start_lightmode()) 
        file.add_separator()

        # add try/except statements for like 3 tabs, if they appear depends on if the command works # TODO: does this still need to be done?
        # not sure what the function should be at this point # TODO: Ummmm what...?
        recents = Menu(file, tearoff=0, postcommand=self.recents.update_recent(pklpath=self.controller.picklepath))
        file.add_cascade(label="Open Recent...", menu=recents)
        numrecents = len(self.recents.recentlist)
        if numrecents == 0:
            recents.add_command(label="no recents found")
        if numrecents >= 1:
            recents.add_command(label=str(Path(self.recents.recentlist[-1][0]).stem), command=lambda: self.open_recent())
        if numrecents >= 2:
            recents.add_command(label="1 " + str(Path(self.recents.recentlist[-2][0]).stem), command=lambda: self.open_recent(2))
        if numrecents >= 3:
            recents.add_command(label="2 " + str(Path(self.recents.recentlist[-3][0]).stem), command=lambda: self.open_recent(3))
        if numrecents >= 4:
            recents.add_command(label="3 " + str(Path(self.recents.recentlist[-4][0]).stem), command=lambda: self.open_recent(4))

        info = Menu(self.menubar, tearoff=0)
        info.add_command(label="Common Issues", command=lambda: self.open_helpmenu()) 
        info.add_command(label="Colmap Info", command=lambda: self.open_helpmenu("colmap.html")) 
        info.add_command(label="MeshLab Info", command=lambda: self.open_helpmenu("meshlab.html"))
    
        recon = Menu(self.menubar, tearoff=0)
        recon.add_command(label="Auto Reconstruction", command=lambda: self.controller.auto_recon()) 
        recon.add_command(label="Restore Point Cloud", command=lambda: self.controller.restore())

        # Add menues as cascades
        self.menubar.add_cascade(label="File", menu=file)
        self.menubar.add_cascade(label="Info", menu=info) 
        self.menubar.add_cascade(label="Reconstruction", menu=recon) 
        self.controller.config(menu=self.menubar)
        self.menubar.entryconfig("Reconstruction", state="disabled")

    # Event handler for the "new project" menu item
        # Should open a dialogue asking the user to selct a working directory
        # Then call controllers new_project method
    def new_project(self):
        projdir = fd.askdirectory(title='Select Workspace', initialdir='/home/')
        if not projdir:
            return
        if ' ' in projdir:
            print("Path must not contain white spaces")
            mb.showerror("Paths cannot contain whitespace                           ")
            return
        self.controller.new_project(projdir)
        #print("in new: " + str(self.controller.picklepath))
        #RecentsManager.update_recent()     # TODO: Important?

    # Event handler for the "open project" menu item
        # Should open a dialogue asking the user to selct a project file
        # Then call controllers open_project method
    def open_project(self, projfile=None):
        if not projfile:
            projfile = fd.askopenfilename(filetypes=[('Choose a project (.pkl) file', '*.pkl')])
            if not projfile:
                return
        self.controller.open_project(Path(projfile))
        
    def open_recent(self,index=1):
        index = -index
        try:
            projfile = self.recents.recentlist[index][0]
            if not projfile:
                return
            self.open_project(projfile)
        except:
            print("file not saved to history") # TODO: is isnt a very informative error message

    # Handler for setting dark mode
    #   changes theme to a dark theme
    #   might be worth adding some flag so that we don't have to switch if we already have one style.
    def start_darkmode(self):
        if (self.controller.styleflag == "dark"):
            return
        self.controller.style = Style("darkly")
        self.controller.styleflag = "dark"
        self.init_common_style()

    def start_lightmode(self):
        if (self.controller.styleflag == "light"):
            return
        self.controller.style = Style("lumen")
        self.controller.styleflag = "light"
        self.init_common_style()

    def init_common_style(self): # TODO: Rename, this isnt super clear cut
        temp = self.controller.swtich_style()
        self.controller.style.configure("TButton", width=16)
        self.controller.style.configure("cancel.TButton", width=30)
        self.controller.style.configure("title.TLabel", font=('Helvetica', 30, "bold"))

        # progress bar # TODO: is this exact same thing in main or am I crazy?
        self.controller.style.layout("prog.Horizontal.TProgressbar",
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar', {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}),
              ('Horizontal.Progressbar.label', {'sticky': ''})])
        self.controller.style.configure("prog.Horizontal.TProgressbar", font=('Helvetica', 11), background="goldenrod1")

        # progress bar progress % text
        if 0 < temp < 100: 
            self.controller.style.configure('prog.Horizontal.TProgressbar', text='{:g} %'.format(temp))
        else:
            return

    # Handler for opening the help menu/docs
    #   can take argument to specify which page to open if it isn't the main page.
    def open_helpmenu(self, docpage = "index.html"):
        try:
            wb.open_new(('file:///' + str(Path(f"docs/_build/html").absolute()) + "/" + docpage).replace("\\","/"))
        except:
            pass
        return