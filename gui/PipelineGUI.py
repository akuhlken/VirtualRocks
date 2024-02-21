import tkinter as tk
import ttkbootstrap as tttk
from PIL import ImageTk, Image
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import pathlib as pl
from tkinter import ttk
from gui.AppWindow import AppWindow
from showinfm import show_in_file_manager

class PipelineGUI(AppWindow):
    
    # GUI constants
    DEFAULT_MAP = pl.Path(f"gui/placeholder/darkmap.jpg").resolve()
    DEFAULT_PREVIEW = pl.Path(f"gui/placeholder/drone.jpg").resolve()

    # temp constants until we have a good way to deal with outliers and can display
    DARK_MAP = pl.Path(f"gui/placeholder/darkmap.jpg").resolve()
    LIGHT_MAP = pl.Path(f"gui/placeholder/map.jpg").resolve()

    def __init__(self, parent, controller, projdir):
        AppWindow.__init__(self, parent, controller)
        self.projdir = projdir
        self.controller = controller
        self.currentmap = self.DEFAULT_MAP
        self.state = 0  # 0 = not started, 1 = matching started, 2 = matching done, 3 = mesher started, 4 = mesher done
        self.setup_layout()
        
    # Setup method for GUI layout and elements
    def setup_layout(self):
        # Layout framework
        left = ttk.Frame(self)
        right = ttk.Frame(self)
        prog = ttk.Frame(left)
        sep = ttk.Frame(right)
        left.pack(side='left', fill='both', anchor="e", expand=True)
        right.pack(side='right', fill='y', anchor="e", expand=False)
        sep.pack(side='left', expand=False)
        prog.pack(side='bottom', fill='x', anchor="s", expand=False)
        
        # control elements
        self.exampleimage = ttk.Label(right)

        self.addphotos = ttk.Button(right, text="Add Photos", command=lambda: self.photos_handler())

        self.numimages = ttk.Label(right, text="Number of images:")
        self.matcher = ttk.Button(right, text="Matcher", command=lambda: self.controller.start_matcher())
        self.setbounds = ttk.Button(right, text="Set Bounds", command=lambda: self.bounds_handler())
        self.outres = ttk.Label(right, text="Output Resulution:")
        self.mesher = ttk.Button(right, text="Mesher", command=lambda: self.controller.start_mesher())
        self.show = ttk.Button(right, text="Show Files", command=lambda: self.show_files())
        self.cancel = ttk.Button(right, text="Cancel", style="cancel.TButton", command=lambda: self.controller.cancel_recon())
        
        # status elements
        self.map = tk.Canvas(left)  # ttk doesn't have a canvas widget, so we can't convert this.
        self.dirtext = ttk.Label(left, text="Project Directory: Test/test/test/test/test")
        self.changebtn = ttk.Button(left, text="Change", command=lambda: self.change_projdir())

        self.logtext = tk.Text(right, width=50, background=self.controller.logbackground)
        scrollbar = ttk.Scrollbar(right)
        self.logtext['yscrollcommand'] = scrollbar.set
        scrollbar['command'] = self.logtext.yview

        # progress bar elements
        self.progresstotal = ttk.Progressbar(prog, length=280, mode='determinate', max=100, style="Horizontal.TProgressbar")
        self.progresstotaltext = ttk.Label(prog, text="Total Progress:")
        self.progress = ttk.Progressbar(prog, length=280, mode='determinate', max=100, style="prog.Horizontal.TProgressbar")
        self.progresstext = ttk.Label(prog, text="Progress on Current Step:")

        # separator, for style
        self.separator = tttk.Separator(right, bootstyle="info", orient="vertical")

        # packing
        self.separator.pack(side="left", fill="y", padx=5)
        self.exampleimage.pack()
        self.addphotos.pack()
        self.numimages.pack()
        self.matcher.pack()
        self.setbounds.pack()
        self.outres.pack()
        self.mesher.pack()
        self.show.pack()
        self.cancel.pack(anchor="s", side="bottom")
        self.logtext.pack(side='left', fill='both', expand=True)
        self.changebtn.pack(side='bottom')
        self.dirtext.pack(side='bottom')
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
        self.show.config(state="disabled")
        self.cancel.config(state="disabled")

    # Event handler for "New" in the dropdown menu
        # Method should first check to make sure nothing is running.
        # Then it should do basically the same thing as the new_project method
        # in StartGUI.
    def new_proj_handler(self):
        projdir = fd.askdirectory(title='select workspace', initialdir='/home/')
        if not projdir:
            return
        if ' ' in projdir:
            print("Path must not contain white spaces")
            mb.showerror("Paths cannot contain whitespace                           ")
            return
        self.controller.new_project(projdir)

    # Event handler for "Start Menu" in the dropdown menu
    def startmenu_handler(self):
        self.controller.config(menu=tk.Menu(self))
        self.controller.start_menu()

    # Event handler for "Add Photos" button
        # Method should open a dialogue prompting the user to select img dir
        # Pass directory to controllers add_photos handler
    def photos_handler(self):
        # starting progress bar
        imgdir = fd.askdirectory(title='select folder of images', initialdir=self.projdir)
        if not imgdir:
            return
        if ' ' in imgdir:
            print("Path must not contain white spaces")
            mb.showerror("Paths cannot contain whitespace                           ")
            return
        self.controller.add_photos(imgdir)
        # updating progress bar
        self.progress.config(value=self.progress["maximum"])
        #self.progresstotal.step(10)
        self.controller.style.configure('prog.Horizontal.TProgressbar', text='100%')

    # Event handler for "Set Bounds" button
        # Method should open a dialogue prompting the user to enter bounds
        # Pass bounds A and B to controllers set_bounds handler
    def bounds_handler(self):
        # progress bar updating:
        self.controller.set_bounds((0,0),(0,0))
        #self.progresstotal.step(1)

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
        self.currentmap = mapdir


    # Method to be called externally for setting example image
    def set_example_image(self, imagefile):
        img = Image.open(imagefile)
        img = img.resize((150, 100), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        self.exampleimage.config(image=img)
        self.exampleimage.image = img

    # Gives the user an option to chnage the main project directory
    #   If no savefile this will refresh and create a new project
    #   If chosen dir has a savefile this will load the existing project
    def change_projdir(self):
        projdir = fd.askdirectory(title='select workspace', initialdir='/home/')
        if not projdir:
            return
        if ' ' in projdir:
            print("Path must not contain white spaces")
            mb.showerror("Paths cannot contain whitespace                           ")
            return
        self.controller.cancel_recon()   
        self.controller.new_project(projdir, self.controller.projectname, self.controller.imgdir)

    def show_files(self):
        show_in_file_manager(str(self.controller.projdir) + "/out")

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