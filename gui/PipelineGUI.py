import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog as fd
import pathlib as pl

class PipelineGUI(tk.Frame):
    
    DEFAULT_MAP = pl.Path(f"gui/tempmap.png").resolve()
    DEFAULT_PREVIEW = pl.Path(f"gui/DJI_0441.jpg").resolve()
    STATE = 0  # 0 = not started, 1 = in progress, 2 = done

    def __init__(self, parent, controller, projpath):
        tk.Frame.__init__(self, parent)
        self.projpath = projpath
        self.controller = controller
        self.create_menu()
        self.setup_layout()
        print(self.projpath)

    def create_menu(self):
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

        left = tk.Frame(self, bg=self.controller.backcolor)
        right = tk.Frame(self, bg=self.controller.backcolor)
        prog = tk.Frame(left, bg=self.controller.backcolor)

        left.pack(side='left', fill='both', anchor="e", expand=True)
        right.pack(side='right', fill='y', anchor="e", expand=False)
        prog.pack(side='bottom', fill='x', anchor="s", expand=False)

        temp3 = tk.Button(prog, height=10, text="[progress]", bg=self.controller.backcolor).pack(fill="both", expand=True)

        # TODO: Keep map image in the middle of its window
        self.map = tk.Canvas(left, bg=self.controller.backcolor)
        self.map.pack(fill='both', expand=True, side='right')
        
        # control elements
        self.panel = tk.Label(right)
        self.panel.pack()
        self.addphotos = tk.Button(right, text="Add Photos", bg=self.controller.buttoncolor, pady=5, padx=5, command=lambda: self.photos_handler())
        self.numimages = tk.Label(right, text="Number of images:", bg=self.controller.backcolor)
        self.setbounds = tk.Button(right, text="Set Bounds", bg=self.controller.buttoncolor, pady=5, padx=5, command=lambda: self.bounds_handler())
        self.outres = tk.Label(right, text="Output Resulution:", bg=self.controller.backcolor)
        self.action = tk.Button(right, text="Start", bg=self.controller.buttoncolor, pady=5, padx=5, command=lambda: self.action_handler())
        self.log = tk.Button(right, text="[Log]", bg=self.controller.backcolor)
        
        self.addphotos.pack()
        self.numimages.pack()
        self.setbounds.pack()
        self.outres.pack()
        self.action.pack()
        self.log.pack(fill="both", expand=True)

        self.setbounds.config(state="disabled")
        self.action.config(state="disabled")

    def photos_handler(self):
        self.controller.add_photos(fd.askdirectory(title='select workspace', initialdir='/home/'))

    def bounds_handler(self):
        self.controller.set_bounds((0,0),(0,0))

    def action_handler(self):
        if self.STATE == 0:
            self.controller.start_recon()
            #self.action.config(text="Cancel")
            return
        if self.STATE == 1:
            self.controller.cancel_recon()
            #self.action.config(text="Start")
            return
        if self.STATE == 2:
            self.controller.export()
            return

    def update_text(self, numimg=None, outres=None):
        # for coden: call with update_text(numimg= NUMBER OF IMAGES) these are optional args
        if numimg:
            self.numimages = "Num images: " + numimg
        if outres:
            self.outres = "Output resolution: " + outres

    def set_map(self, mapdir):
        image = ImageTk.PhotoImage(Image.open(mapdir))
        self.map_image_id = self.map.create_image(0, 0, image=image, anchor='nw')
        self.map_image = mapdir
        self.map.bind('<Configure>', self.resizer)

    def set_example_image(self, imagedir):
        img = Image.open(imagedir)
        img = img.resize((150, 100), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        self.panel.config(image=img)
        self.panel.image = img

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

        









