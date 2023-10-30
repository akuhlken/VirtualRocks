import tkinter as tk           
from tkinter import font as tkfont  

from PipelineGUI import PipelineGUI
from StartGUI import StartGUI

class main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("1000x500")
        self.title("VirtualRocks")
        self.title_font = tkfont.Font(family='Helvetica', size=24, weight="bold", slant="italic")

        # container is a stack of fames (aka out two main pages)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        frame = StartGUI(parent=self.container, controller=self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def start_project(self, projpath):
        frame = PipelineGUI(self.container, self, projpath)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

if __name__ == "__main__":
    app = main()
    app.mainloop()