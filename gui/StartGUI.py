import tkinter as tk
from tkinter import filedialog as fd

def get_dir():
    return fd.askdirectory(title='select workspace', initialdir='/home/')

def new_project():
    projpath = get_dir()
    return projpath

def open_project():
    projpath = get_dir()
    return projpath

class StartGUI(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Project:", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        middleframe = tk.Frame(self)
        middleframe.place(anchor="c", relx=.5, rely=.5)

        newBtn = tk.Button(middleframe, height=10, width=20, text="New", command=lambda: controller.start_project(new_project()))
        openBtn = tk.Button(middleframe, height=10, width=20, text="Open", command=lambda: controller.start_project(open_project()))

        newBtn.pack(padx=20, side='left')
        openBtn.pack(padx=20, side='right')
        