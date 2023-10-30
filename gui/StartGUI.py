import tkinter as tk
from tkinter import filedialog as fd

class StartGUI(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Choose Project:", font=controller.font, bg=controller.backcolor)
        label.pack(side="top", fill="x", pady=10)
        self.config(bg=controller.backcolor)

        middleframe = tk.Frame(self, bg=controller.backcolor)
        middleframe.place(anchor="c", relx=.5, rely=.5)

        newBtn = tk.Button(middleframe, height=10, width=20, text="New", bg=controller.buttoncolor, command=lambda: self.new_project())
        openBtn = tk.Button(middleframe, height=10, width=20, text="Open", bg=controller.buttoncolor, command=lambda: self.open_project())

        newBtn.pack(padx=20, side='left')
        openBtn.pack(padx=20, side='right')

    def get_dir(self):
        return fd.askdirectory(title='select workspace', initialdir='/home/')
    
    def get_file(self):
        # Load specific project file
        pass
        
    def new_project(self):
        projdir = self.get_dir()
        if not projdir:
            return
        self.controller.new_project(projdir)

    def open_project(self):
        # TODO: eventually this should select a specific save file, not just a dir
        projfile = "error" # self.get_file()
        if not projfile:
            return
        self.controller.open_project(projfile)


        