import tkinter as tk
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
        menubar = tk.Menu(self) 

        file = tk.Menu(menubar, tearoff=0)  
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
        styles.add_command(label="Dark", command=lambda: self.controller.start_darkmode())
        styles.add_command(label="Light", command=lambda: self.controller.start_lightmode()) 
        styles.add_command(label="not Goblin", command=lambda: self.controller.start_goblinmode()) 
        styles.add_command(label="Pick Color")

        file.add_separator() 
        file.add_command(label="Exit", command=self.quit)  

        info = tk.Menu(menubar, tearoff=0)
        info.add_command(label="Common Issues", command=lambda: self.controller.open_helpmenu()) 
        info.add_command(label="Colmap Info", command=lambda: self.controller.open_helpmenu("colmap.html")) 
        info.add_command(label="MeshLab Info", command=lambda: self.controller.open_helpmenu("meshlab.html")) 
        info.add_command(label="Pasta Recipes") 

        menubar.add_cascade(label="File", menu=file)  
        menubar.add_cascade(label="Info", menu=info) 

        self.controller.config(menu=menubar)

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