import tkinter as tk
#import ttkbootstrap as tttk
from PIL import ImageTk, Image
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import pathlib as pl
from tkinter import ttk

class PipelineGUI(ttk.Frame):
    
    # GUI constants
    DEFAULT_MAP = pl.Path(f"gui/placeholder/map.jpg").resolve()
    DEFAULT_PREVIEW = pl.Path(f"gui/placeholder/drone.jpg").resolve()

    def __init__(self, parent, controller, progdir):
        ttk.Frame.__init__(self, parent)
        self.progdir = progdir
        self.controller = controller
        self.state = 0  # 0 = not started, 1 = matching started, 2 = matching done, 3 = mesher started, 4 = mesher done
        self.create_menu()
        self.setup_layout()

    # Settup method for top menu bar
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
        info.add_command(label="Common Issues") 
        info.add_command(label="Colmap Info") 
        info.add_command(label="MeshLab Info") 
        info.add_command(label="Pasta Recipes") 

        menubar.add_cascade(label="File", menu=file)  
        menubar.add_cascade(label="Info", menu=info)  

        self.controller.config(menu=menubar)

    # Setup method for GUI layout and elements
    def setup_layout(self):

        # Layout framework
        left = ttk.Frame(self)
        right = ttk.Frame(self)
        prog = ttk.Frame(left)
        left.pack(side='left', fill='both', anchor="e", expand=True)
        right.pack(side='right', fill='y', anchor="e", expand=False)
        prog.pack(side='bottom', fill='x', anchor="s", expand=False)
        
        # control elements
        self.exampleimage = ttk.Label(right)
        self.exampleimage.pack()

        self.addphotos = ttk.Button(right, text="Add Photos", command=lambda: self.photos_handler())

        self.numimages = ttk.Label(right, text="Number of images:")
        self.matcher = ttk.Button(right, text="Matcher", command=lambda: self.controller.start_matcher())
        self.setbounds = ttk.Button(right, text="Set Bounds", command=lambda: self.bounds_handler())
        self.outres = ttk.Label(right, text="Output Resulution:")
        self.mesher = ttk.Button(right, text="Mesher", command=lambda: self.controller.start_mesher())
        self.export = ttk.Button(right, text="Export", command=lambda: self.controller.export())
        self.cancel = ttk.Button(right, text="Cancel", command=lambda: self.controller.cancel_recon())
        
        # status elements
        self.map = tk.Canvas(left, bg=self.controller.backcolor)  # ttk doesn't have a canvas widget, so we can't convert this.

        self.logtext = tk.Text(right, width=50)
        scrollbar = ttk.Scrollbar(right)
        self.logtext['yscrollcommand'] = scrollbar.set
        scrollbar['command'] = self.logtext.yview

        # progress bar elements
        # TODO: change how the label updating of the bottom bar works.
        self.progresstotal = ttk.Progressbar(prog, length=280, mode='determinate', max=100, style="Horizontal.TProgressbar")
        self.progresstotaltext = ttk.Label(prog, text="Total Progress:")
        self.progress = ttk.Progressbar(prog, length=280, mode='determinate', max=100, style="prog.Horizontal.TProgressbar")
        self.progresstext = ttk.Label(prog, text="Progress on Current Step:")

        # packing
        self.addphotos.pack()
        self.numimages.pack()
        self.matcher.pack()
        self.setbounds.pack()
        self.outres.pack()
        self.mesher.pack()
        self.export.pack()
        self.logtext.pack(side='left', fill='both', expand=True)
        self.cancel.pack()
        self.map.pack(fill='both', expand=True, side='right')

        self.progresstotaltext.pack()
        self.progresstotal.pack(fill="both", expand=True)
        self.progresstext.pack()
        self.progress.pack(fill="both", expand=True)

        scrollbar.pack(side='right', fill='y')
        
        # dissable buttons
        self.matcher.config(state="disabled")
        self.setbounds.config(state="disabled")
        self.matcher.config(state="disabled")
        self.mesher.config(state="disabled")
        self.export.config(state="disabled")
        self.cancel.config(state="disabled")

    # Event handler for "Add Photos" button
        # Method should open a dialogue prompting the user to select img dir
        # Pass directory to controllers add_photos handler
    def photos_handler(self):
        # starting progress bar
        self.progresstotal.stop()
        self.progresstext.config(text="Image Loading:")
        self.progress.config(value=0)

        imgdir = fd.askdirectory(title='select folder of images', initialdir=self.progdir)
        if not imgdir:
            return
        if ' ' in imgdir:
            print("Path must not contain white spaces")
            mb.showerror("Paths cannot contain whitespace                           ")
            return
        self.controller.add_photos(imgdir)
        # updating progress bar
        self.progress.config(value=self.progress["maximum"])
        self.progresstotal.step(10)
        self.controller.style.configure('prog.Horizontal.TProgressbar', text='100%')

    # Event handler for "Set Bounds" button
        # Method should open a dialogue prompting the user to enter bounds
        # Pass bounds A and B to controllers set_bounds handler
    def bounds_handler(self):
        # progress bar updating:
        self.progress.stop()
        self.progresstext.config(text="Handling Bounds:")
        self.progress.config(value=6)

        self.controller.set_bounds((0,0),(0,0))
        self.progresstotal.step(1)

    # Method to be called externally for updating text related to user input
    def update_text(self, numimg=None, outres=None):
        if numimg:
            self.numimages.config(text=f"Num images: {numimg}")
        if outres:
            self.outres.config(text=f"Output resolution: {outres}")

    # Method to be called externally for setting map image in GUI
    def set_map(self, mapdir):
        image = ImageTk.PhotoImage(Image.open(mapdir))
        self.map_image_id = self.map.create_image(0, 0, image=image, anchor='nw')
        self.map_image = mapdir
        self.map.bind('<Configure>', self._resizer)

    # Method to be called externally for setting example image
    def set_example_image(self, imagefile):
        img = Image.open(imagefile)
        img = img.resize((150, 100), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        self.exampleimage.config(image=img)
        self.exampleimage.image = img

    # Event handler to be called whenever the window is resized
    #   Updates and scales the map image with window
    def _resizer(self, e):
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