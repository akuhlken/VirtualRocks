import tkinter as tk
from tkinter import filedialog as fd

class StartGUI(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Project:", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        middleframe = tk.Frame(self)
        middleframe.place(anchor="c", relx=.5, rely=.5)

        newBtn = tk.Button(middleframe, height=10, width=20, text="New", command=lambda: self.new_project())
        openBtn = tk.Button(middleframe, height=10, width=20, text="Open", command=lambda: self.open_project())

        newBtn.pack(padx=20, side='left')
        openBtn.pack(padx=20, side='right')

    def get_dir(self):
        return fd.askdirectory(title='select workspace', initialdir='/home/')
        
    def new_project(self):
        projpath = self.get_dir()
        if not projpath:
            return
        self.controller.start_project(projpath)

    def open_project(self):
        # TODO: eventually this should select a specific save file, not just a dir
        projpath = self.get_dir()
        if not projpath:
            return
        self.controller.start_project(projpath)

        