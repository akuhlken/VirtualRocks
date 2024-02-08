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
        self.menubar = tk.Menu(self) 

        file = tk.Menu(self.menubar, tearoff=0)  
        file.add_command(label="Back to Start", command=lambda: self.controller.start_menu())
        file.add_command(label="New", command=lambda: self.new_project())  
        #file.add_command(label="New", command=lambda: self.controller.StartGUI.new_project())  
            # check if the user has done any work on the current
            # project they're working on and if they want to save,
            # then make a new file like how we do it from start.
        file.add_command(label="Open", command=lambda: self.open_project())
        #file.add_command(label="Open", command=lambda: self.controller.open_project()) 

        file.add_command(label="Save")  
        file.add_command(label="Save as")    
        file.add_separator()  
 
        # change to an option menu so you can see what you've selected (too hard rn)
        styles = tk.Menu(file, tearoff=0)
        file.add_cascade(label="Set Style", menu=styles)
        styles.add_command(label="Dark", command=lambda: self.start_darkmode())
        styles.add_command(label="Light", command=lambda: self.start_lightmode()) 
        styles.add_command(label="chaos", command=lambda: self.start_goblinmode()) 

        file.add_separator()
        file.add_command(label="Recents...") 
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
        projdir = fd.askdirectory(title='select workspace', initialdir='/home/')
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
    def open_project(self):
        projfile = fd.askopenfilename(filetypes=[('Choose a project.pkl file', '*.pkl')])
        if not projfile:
            return
        self.controller.open_project(projfile)

    # Handler for setting dark mode
    #   changes theme to a dark theme
    #   might be worth adding some flag so that we don't have to switch if we already have one style.
    def start_darkmode(self):
        if (self.controller.styleflag == "dark"):
            return
        self.controller.style = tttk.Style("darkly")
        self.controller.styleflag = "dark"

    def start_lightmode(self):
        if (self.controller.styleflag == "light"):
            return
        self.controller.style = tttk.Style("lumen")
        self.controller.styleflag = "light"
        self.controller.style.configure("TButton", width=16)
        self.controller.style.configure("cancel.TButton", width=30)

    def start_goblinmode(self):
        if (self.controller.styleflag == "goblin"):
            return
        self.controller.style = tttk.Style(theme="goblinmode")
        self.controller.styleflag = "goblin"
        self.controller.style.configure("TButton", width=16)
        self.controller.style.configure("cancel.TButton", width=30)

    # Handler for opening the help menu/docs
    #   can take argument to specify which page to open if it isn't the main page.
    def open_helpmenu(self, docpage = "index.html"):
        try:
            wb.open_new(('file:///' + str(pl.Path(f"docs/_build/html").absolute()) + "/" + docpage).replace("\\","/"))
        except:
            pass
        return