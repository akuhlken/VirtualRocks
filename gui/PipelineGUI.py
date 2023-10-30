import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
import os

class PipelineGUI(tk.Frame):

    def __init__(self, parent, controller, projpath):
        tk.Frame.__init__(self, parent)
        self.projpath = projpath
        self.controller = controller
        self.creat_menu()
        self.setup_layout()
        print(self.projpath)

    def creat_menu(self):
        menubar = tk.Menu(self)  

        file = tk.Menu(menubar, tearoff=0)  
        file.add_command(label="New")  
        file.add_command(label="Open")  
        file.add_command(label="Save")  
        file.add_command(label="Save as")    
        file.add_separator()  
        file.add_command(label="Exit", command=self.quit)  
        
        info = tk.Menu(menubar, tearoff=0)

        menubar.add_cascade(label="File", menu=file)  
        menubar.add_cascade(label="Info", menu=info)  

        self.controller.config(menu=menubar)

    def setup_layout(self):

        mapframe = tk.Frame(self, highlightbackground="black", highlightthickness=1)
        progressframe = tk.Frame(self, highlightbackground="black", highlightthickness=1)
        controlframe = tk.Frame(self, highlightbackground="black", highlightthickness=1)
        logframe = tk.Frame(self, highlightbackground="black", highlightthickness=1)

        mapframe.grid(row=0, column=0, sticky="nsew")
        progressframe.grid(row=1, column=0, sticky="nsew")
        controlframe.grid(row=0, column=1, sticky="nsew")
        logframe.grid(row=1, column=1, sticky="nsew")

        self.rowconfigure(0, weight=5, minsize=20)
        self.rowconfigure(1, weight=1, minsize=10)
        self.columnconfigure(0, weight=5, minsize=20)
        self.columnconfigure(1, weight=1, minsize=5)

        # view elements
        MAP_PLACEHOLDER = tk.Button(mapframe, text="[map]").pack(fill="both", expand=True)
        PROGRESS_PLACEHOLDER = tk.Button(progressframe, text="[Progress Bar]").pack(fill="both", expand=True)

        # control elements
        self.img = Image.open("/home/kuhlkena/Documents/GitHub/VirtualRocks/gui/DJI_0441.jpg")
        self.img = self.img.resize((250, 250), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        panel = tk.Label(controlframe, image=self.img)
        panel.image = self.img
        panel.pack(fill="both", expand=True)
        self.addphotos = tk.Button(controlframe, text="Add Photos", command=lambda: self.add_images).pack(fill="both", expand=True)
        self.numimages = tk.Label(controlframe, text="Number of images:").pack()
        self.setbounds = tk.Button(controlframe, text="Set Bounds", command=lambda: self.set_bounds()).pack(fill="both", expand=True)
        self.outres = tk.Label(controlframe, text="Output Resulution:").pack()
        self.action = tk.Button(controlframe, text="Start Reconstruction", command=lambda: self.start_recon).pack(fill="both", expand=True)
        LOG_PLACEHOLDER = tk.Button(logframe, text="[Log]").pack(fill="both", expand=True)

        # TODO: dissable bounds and action button
        

    def add_images(self):
        # TODO: get images
        # self.numimages["text"] = "Num Images: VAL"
        pass

    def set_bounds(self):
        pass

    def start_recon(self):
        pass
        # TODO: call apropriate scripts

        









