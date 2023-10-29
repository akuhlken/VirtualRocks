import tkinter as tk           
from tkinter import font as tkfont  

from PipelineGUI import PipelineGUI
from StartGUI import StartGUI

class main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("1920x1080")
        self.title("VirtualRocks")
        self.title_font = tkfont.Font(family='Helvetica', size=24, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        """ startFrame = StartGUI(parent=container, controller=self)
        self.frames["StartGUI"] = startFrame
        startFrame.grid(row=0, column=0, sticky="nsew")
 """            
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