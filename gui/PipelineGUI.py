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

        self.rowconfigure(0, weight=5)
        self.columnconfigure(0, weight=5)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

        # view elements
        MAP_PLACEHOLDER = tk.Button(mapframe, text="[map]").pack(fill="both", expand=True)
        PROGRESS_PLACEHOLDER = tk.Button(progressframe, text="[Progress Bar]").pack(fill="both", expand=True)

        # control elements
        img = Image.open("/home/kuhlkena/Documents/GitHub/VirtualRocks/gui/DJI_0441.jpg")
        img = img.resize((250, 250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(controlframe, image=img)
        panel.image = img
        panel.pack(fill="both", expand=True)
        addphotos = tk.Button(controlframe, text="Add Photos").pack(fill="both", expand=True)
        setbounds = tk.Button(controlframe, text="Set Bounds").pack(fill="both", expand=True)
        action = tk.Button(controlframe, text="Start Reconstruction").pack(fill="both", expand=True)
        LOG_PLACEHOLDER = tk.Button(logframe, text="[Log]").pack(fill="both", expand=True)

        









