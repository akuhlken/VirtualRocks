import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog as fd
import pathlib as pl
# might have to import ttk for progressbar class.
from tkinter import ttk

class PipelineGUI(tk.Frame):
    
    # GUI constants
    DEFAULT_MAP = pl.Path(f"gui/placeholder/map.jpg").resolve()
    DEFAULT_PREVIEW = pl.Path(f"gui/placeholder/drone.jpg").resolve()

    def __init__(self, parent, controller, projpath):
        tk.Frame.__init__(self, parent)
        self.projpath = projpath
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
        menubar.add_cascade(label="File", menu=file)  
        menubar.add_cascade(label="Info", menu=info)  

        self.controller.config(menu=menubar)

    # Setup method for GUI layout and elements
    def setup_layout(self):

        ttk.Style().configure("TButton", padding=6)

        # Layout framework
        left = tk.Frame(self, bg=self.controller.backcolor)
        right = tk.Frame(self, bg=self.controller.backcolor)
        prog = tk.Frame(left, bg=self.controller.backcolor)
        left.pack(side='left', fill='both', anchor="e", expand=True)
        right.pack(side='right', fill='y', anchor="e", expand=False)
        prog.pack(side='bottom', fill='x', anchor="s", expand=False)
        
        # control elements
        self.panel = tk.Label(right)
        self.panel.pack()
        self.addphotos = tk.Button(right, text="Add Photos", bg=self.controller.buttoncolor, pady=5, padx=5, command=lambda: self.photos_handler())
        self.numimages = tk.Label(right, text="Number of images:", bg=self.controller.backcolor)
        self.matcher = tk.Button(right, text="Start Matcher", bg=self.controller.buttoncolor, pady=5, padx=5, command=lambda: self.matcher_handler())
        self.setbounds = tk.Button(right, text="Set Bounds", bg=self.controller.buttoncolor, pady=5, padx=5, command=lambda: self.bounds_handler())
        self.outres = tk.Label(right, text="Output Resulution:", bg=self.controller.backcolor)
        self.mesher = tk.Button(right, text="Start Mesher", bg=self.controller.buttoncolor, pady=5, padx=5, command=lambda: self.mesher_handler())

        # status elements
        self.log = tk.Button(right, text="[Log]", bg=self.controller.backcolor)
        # TODO: Coden >:)
        #self.progress = tk.Button(prog, height=10, text="[progress, in progress]", bg=self.controller.backcolor)
        self.progress = ttk.Progressbar(prog, length=280, mode='determinate', max=300)
        self.map = tk.Canvas(left, bg=self.controller.backcolor)

        # packing
        self.addphotos.pack()
        self.numimages.pack()
        self.matcher.pack()
        self.setbounds.pack()
        self.outres.pack()
        self.mesher.pack()
        self.log.pack(fill="both", expand=True)
        self.progress.pack(fill="both", expand=True, anchor='center')
        self.map.pack(fill='both', expand=True, side='right')
        
        # dissable buttons
        self.setbounds.config(state="disabled")
        self.matcher.config(state="disabled")
        self.mesher.config(state="disabled")

    # Event handler for "Add Photos" button
        # Method should open a dialogue prompting the user to select img dir
        # Pass directory to controllers add_photos handler
    def photos_handler(self):
        self.controller.add_photos(fd.askdirectory(title='select image directory', initialdir='/home/'))

    # Event handler for "Set Bounds" button
        # Method should open a dialogue prompting the user to enter bounds
        # Pass bounds A and B to controllers set_bounds handler
    def bounds_handler(self):
        self.controller.set_bounds((0,0),(0,0))

    # Event handler for bottom mesher button
        # Method should react based on the current state of the GUI
        # and call the correct method in controller
    def matcher_handler(self):
        if self.state == 0:
            self.controller.start_matcher()
            self.progress.step(10)
            return
        if self.state == 1:
            self.controller.cancel_recon()
            self.progress.stop()
            return

    # Event handler for bottom mesher button
        # Method should react based on the current state of the GUI
        # and call the correct method in controller
    def mesher_handler(self):
        if self.state == 2:
            self.controller.start_mesher()
            return
        if self.state == 3:
            self.controller.cancel_recon()
            return
        if self.state == 4:
            self.controller.export()
            return        

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
        self.panel.config(image=img)
        self.panel.image = img

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

        









