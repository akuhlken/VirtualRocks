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

        self.map_image = r'C:\Users\akuhl\Desktop\GitHub\VirtualRocks\gui\tempmap.png'

        left = tk.Frame(self, highlightbackground="black", highlightthickness=1)
        right = tk.Frame(self, highlightbackground="black", highlightthickness=1)
        prog = tk.Frame(left, highlightbackground="black", highlightthickness=1)
        log = tk.Frame(right, highlightbackground="black", highlightthickness=1)

        left.pack(side='left', fill='both', anchor="e", expand=True)
        right.pack(side='right', fill='y', anchor="e", expand=False)
        prog.pack(side='bottom', fill='x', anchor="s", expand=False)

        temp3 = tk.Button(prog, height=10, text="[progress]").pack(fill="both", expand=True)

        image = ImageTk.PhotoImage(Image.open(self.map_image))
        imageWidth = image.width()
        imageHeight = image.height()

        # TODO: Keep map image in the middle of its window
        self.map = tk.Canvas(left)
        self.map.pack(fill='both', expand=True, side='right')
        self.map_image_id = self.map.create_image(0, 0, image=image, anchor='nw')
        self.map.bind('<Configure>', self.resizer)

        # control elements
        self.img = Image.open(r"C:\Users\akuhl\Desktop\GitHub\VirtualRocks\gui\DJI_0441.jpg")
        self.img = self.img.resize((150, 100), Image.LANCZOS)
        self.img = ImageTk.PhotoImage(self.img)
        panel = tk.Label(right, image=self.img)
        panel.image = self.img
        panel.pack()
        self.addphotos = tk.Button(right, text="Add Photos", command=lambda: self.add_images).pack()
        self.numimages = tk.Label(right, text="Number of images:").pack()
        self.setbounds = tk.Button(right, text="Set Bounds", command=lambda: self.set_bounds()).pack()
        self.outres = tk.Label(right, text="Output Resulution:").pack()
        self.action = tk.Button(right, text="Start Reconstruction", command=lambda: self.start_recon).pack()
        self.log = tk.Button(right, text="Log", command=lambda: self.start_recon).pack(fill="both", expand=True)

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

    def resizer(self, e):
        global image1, resized_image, new_image
        image1 = Image.open(self.map_image)
        width_scale = e.width / image1.width
        height_scale = e.height / image1.height
        scale = min(width_scale, height_scale)

        new_width = int(image1.width * scale)
        new_height = int(image1.height * scale)

        resized_image = image1.resize((new_width, new_height), Image.Resampling.LANCZOS)
        new_image = ImageTk.PhotoImage(resized_image)
        self.map.itemconfigure(self.map_image_id, image=new_image)

        









