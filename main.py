import tkinter as tk           
from tkinter import font as tkfont  
import scripts.getMeta as meta
from gui.PipelineGUI import PipelineGUI
from gui.StartGUI import StartGUI

class main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Controller Variables
        self.projfile = ""
        self.imagedir = ""
        self.A = (0,0)
        self.B = (0,0)
        self.map = None
        self.image = None

        self.minsize(500, 300)
        self.geometry("1000x500")
        self.title("VirtualRocks")

        # Application styling
        self.font = tkfont.Font(family='Arial', size=24, weight="bold")
        self.buttoncolor = "#ffffff"
        self.backcolor = "#ffffff"

        # container is a stack of fames (aka out two main pages)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        frame = StartGUI(parent=self.container, controller=self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def new_project(self, projdir):
        # TODO: self.projfile = progjdir + new file
        frame = PipelineGUI(self.container, self, projdir)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.set_map(frame.DEFAULT_MAP)
        frame.set_example_image(frame.DEFAULT_PREVIEW)
        frame.tkraise()

    def open_project(self, projfile):
        # TODO: loading of old project
        print("NOT YET COMPLETED")

    def add_photos(self, imagedir):
        self.imagedir = imagedir
        meta.iterate(self.imagedir)

    def set_bounds(self, A, B):
        self.A = A
        self.B = B

    def start_recon(self):
        pass

    def cancel_recon(self):
        pass

    def export(self):
        pass

    def update_log(self):
        pass

    def update_progress(self):
        pass

    def update_map(self):
        pass


if __name__ == "__main__":
    app = main()
    app.mainloop()