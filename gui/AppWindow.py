import tkinter as tk
import ttkbootstrap as tttk 
import webbrowser as wb
import pathlib as pl
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import ttk

class AppWindow(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_menu()

    # Setup method for top menu bar
    def create_menu(self):
        # need to be able to refresh menu
        self.menubar = tk.Menu(self) #postcommand=self.controller.update_recent(menuupdate=True) 

        file = tk.Menu(self.menubar, tearoff=0)  
        file.add_command(label="Back to Start", command=lambda: self.controller.start_menu())
        file.add_command(label="New", command=lambda: self.new_project())  
        #file.add_command(label="New", command=lambda: self.controller.StartGUI.new_project())  
            # check if the user has done any work on the current
            # project they're working on and if they want to save,
            # then make a new file like how we do it from start.
        file.add_command(label="Open", command=lambda: self.open_project())

        file.add_command(label="Save")  
        file.add_command(label="Save as")    
        file.add_separator()  
 
        # change to an option menu so you can see what you've selected (too hard rn)
        styles = tk.Menu(file, tearoff=0)
        file.add_cascade(label="Set Style...", menu=styles)
        styles.add_command(label="Dark", command=lambda: self.start_darkmode())
        styles.add_command(label="Light", command=lambda: self.start_lightmode()) 
        styles.add_command(label="chaos", command=lambda: self.start_goblinmode()) 
        file.add_separator()

        # add try/except statements for like 3 tabs, if they appear depends on if the command works
        # not sure what the function should be at this point
        recents = tk.Menu(file, tearoff=0, postcommand=self.controller.update_recent())
        file.add_cascade(label="Open Recent...", menu=recents)
        numrecents = len(self.controller.recentlist)
        if numrecents == 0:
            recents.add_command(label="no recents found")
        if numrecents >= 1:
            recents.add_command(label="Print All Recents", command=lambda: self.controller.get_recent()) # should remove this command, for testing only.
            recents.add_separator()
            recents.add_command(label=str(pl.Path(self.controller.recentlist[-1]).stem), command=lambda: self.open_recent())
        if numrecents >= 2:
            recents.add_command(label="1 " + str(pl.Path(self.controller.recentlist[-2]).stem), command=lambda: self.open_recent(2))
        if numrecents >= 3:
            recents.add_command(label="2 " + str(pl.Path(self.controller.recentlist[-3]).stem), command=lambda: self.open_recent(3))
        if numrecents >= 4:
            recents.add_command(label="3 " + str(pl.Path(self.controller.recentlist[-4]).stem), command=lambda: self.open_recent(4))


        file.add_separator()
        file.add_command(label="Exit", command=self.quit)  

        info = tk.Menu(self.menubar, tearoff=0)
        info.add_command(label="Common Issues", command=lambda: self.open_helpmenu()) 
        info.add_command(label="Colmap Info", command=lambda: self.open_helpmenu("colmap.html")) 
        info.add_command(label="MeshLab Info", command=lambda: self.open_helpmenu("meshlab.html"))
    
        recon = tk.Menu(self.menubar, tearoff=0)
        recon.add_command(label="Auto Reconstruction", command=lambda: self.controller.auto_recon()) 
        recon.add_command(label="Advanced Options", command=lambda: self.controller.options()) 

        self.menubar.add_cascade(label="File", menu=file)
        self.menubar.add_cascade(label="Info", menu=info) 
        self.menubar.add_cascade(label="Reconstruction", menu=recon) 
        self.controller.config(menu=self.menubar)
        self.menubar.entryconfig("Reconstruction", state="disabled")

    # Event handler for the "new project" button
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

    # Event handler for the "open project" button
        # Should open a dialogue asking the user to selct a project save file
        # Then call controllers open_project method
    def open_project(self, projfile=None, menuupdate=False):
        if menuupdate:
            self.controller.update_recent(menuupdate=True)
            return
        if not projfile:
            projfile = fd.askopenfilename(filetypes=[('Choose a project (.pkl) file', '*.pkl')])
        if not projfile:
            return
        self.controller.open_project(projfile)
        
    def open_recent(self,index=1):
        index = -index # need negation of index because most recent is at the end.
        try:
            projfile = self.controller.recentlist[index]
            if not projfile:
                return
            self.open_project(projfile)
        except:
            print("file not saved to history")

    # Handler for setting dark mode
    #   changes theme to a dark theme
    #   might be worth adding some flag so that we don't have to switch if we already have one style.
    def start_darkmode(self):
        if (self.controller.styleflag == "dark"):
            return
        self.controller.style = tttk.Style("darkly")
        self.controller.styleflag = "dark"
        self.init_common_style()

    def start_lightmode(self):
        if (self.controller.styleflag == "light"):
            return
        self.controller.style = tttk.Style("lumen")
        self.controller.styleflag = "light"
        self.init_common_style()

    def start_goblinmode(self):
        if (self.controller.styleflag == "goblin"):
            return
        self.controller.style = tttk.Style(theme="goblinmode")
        self.controller.styleflag = "goblin"
        self.init_common_style()

    def init_common_style(self):
        temp = self.controller.swtich_style()
        self.controller.style.configure("TButton", width=16)
        self.controller.style.configure("cancel.TButton", width=30)
        self.controller.style.configure("title.TLabel", font=('Helvetica', 30, "bold"))

        # progress bar
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
            wb.open_new(('file:///' + str(pl.Path(f"docs/_build/html").absolute()) + "/" + docpage).replace("\\","/"))
        except:
            pass
        return