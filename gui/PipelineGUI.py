from tkinter import Canvas, Text, END, Button as tkButton
from tkinter.ttk import Frame, Label, Button, Scrollbar, Progressbar
from ttkbootstrap import Separator
from tkinter import filedialog as fd, messagebox as mb
from PIL import ImageTk, Image
from pathlib import Path
from gui.AppWindow import AppWindow
from gui.BoundsDialog import BoundsDialog
from showinfm import show_in_file_manager

# TODO: header comments
class PipelineGUI(AppWindow):
    
    # GUI constants
    DEFAULT_CHART = Path(f"gui/placeholder/blankchart.jpg").resolve()
    DEFAULT_PREVIEW = Path(f"gui/placeholder/drone.jpg").resolve()

    def __init__(self, parent, controller, projdir, recents):
        """
        description of the whole class

        Args:
            parent (type?): what is it?
            controller (type?): what is it?
            projdir (type?): what is it?
            recents (type?): what is it?
        """
        AppWindow.__init__(self, parent, controller, recents)
        self.setup_layout()
        self.projdir = projdir
        self.controller = controller
        self.currentchart = self.DEFAULT_CHART
        self.bind("<<RefreshChart>>", self._refresh_chart)

    # Setup method for GUI layout and elements
    def setup_layout(self):
        """
        description, sets everything up. probs needs a lot of desc.
        """
        ### Frames:
        self.left = Frame(self)
        right = Frame(self)
        prog = Frame(self.left)

        # packing the main frames
        self.left.pack(side='left', fill='both', anchor="e", expand=True)
        right.pack(side='right', fill='y', anchor="e", expand=False)
        prog.pack(side='bottom', fill='x', anchor="s", expand=False)
        
        # subframes, for alignment + spacing
        chartbuttonsframe = Frame(self.left, padding='3p')
        addphotosframe = Frame(right, padding='3p')
        boundsframe = Frame(right, padding='3p')
        showframe = Frame(right, padding='3p')

        
        ### Right: elements + buttons on the right bar
        self.exampleimage = Label(right)
        self.addphotos = Button(addphotosframe, text="1: Add Photos", command=lambda: self.photos_handler())
        self.numimages = Label(right, text="Number of images:")
        self.matcher = Button(right, text="2: Matcher", command=lambda: self.controller.start_matcher())
        self.trimbounds = Button(boundsframe, text="Trim", width=8, command=lambda: self.bounds_handler())
        self.resetbounds = Button(boundsframe, text="Reset", width=8, command=lambda: self.controller.restore())
        self.mesher = Button(right, text="3: Mesher", command=lambda: self.controller.start_mesher())
        self.show = Button(showframe, text="4: Show Files", command=lambda: self.show_files())

        # the log, scrollbar, and cancel button for recon.
        self.logtext = Text(right, width=50, background=self.controller.logbackground)
        scrollbar = Scrollbar(right)
        self.logtext['yscrollcommand'] = scrollbar.set
        scrollbar['command'] = self.logtext.yview
        self.cancel = Button(right, text="Cancel", style="cancel.TButton", command=lambda: self.controller.cancel_recon())
        

        ### Left: charts and progress
        self.temp = ImageTk.PhotoImage(Image.open(self.DEFAULT_CHART))
        self.chart = Canvas(self.left)
        self.chart_image_id = self.chart.create_image(0, 0, image=self.temp, anchor='nw')
        self.chart.bind('<Configure>', self._resizer)
        self.previewcloud = Button(chartbuttonsframe, width=20, text="Preview Point Cloud")  # TODO: need to add the handler/command to open the preview.
        self.chartswitch = Button(chartbuttonsframe, width=20, text="Switch Chart")  # TODO: need to add the handler/command to switch chart

        # progress bar frame elements
        self.dirtext = Label(prog, text="Project Directory: Test/test/test/test/test")
        self.changebtn = Button(prog, text="Change", command=lambda: self.change_projdir())
        self.progresstotaltext = Label(prog, text="Total Progress:")
        self.progresstotal = Progressbar(prog, length=280, mode='determinate', max=100, style="Horizontal.TProgressbar")
        self.progresstext = Label(prog, text="Progress on Current Step:")
        self.progress = Progressbar(prog, length=280, mode='determinate', max=100, style="prog.Horizontal.TProgressbar")


        ### Misc style elements:
        # separators (bars)
        self.vertseparator = Separator(right, bootstyle="info", orient="vertical")
        self.horiseparator = Separator(prog, bootstyle="info", orient="horizontal")

        # spacers
        boundsspacer = Label(boundsframe, text=" ", font=('Helvetica', 1))
        chartbuttonspacer = Label(chartbuttonsframe, text=" ", font=('Helvetica', 1))


        ### packing
        ## Right:
        self.vertseparator.pack(side="left", fill="y", padx=5)
        self.exampleimage.pack()
        self.numimages.pack()
        addphotosframe.pack()
        self.addphotos.pack()
        self.matcher.pack()
        # bounds buttons, gridded to be inline
        boundsframe.pack()
        self.trimbounds.grid(row=0, column=0)
        boundsspacer.grid(row=0, column=1)
        self.resetbounds.grid(row=0, column=2)
        self.mesher.pack()
        showframe.pack()
        self.show.pack()
        self.cancel.pack(anchor="s", side="bottom")
        self.logtext.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        ## Left:
        # progress bar
        self.horiseparator.pack(side='top', fill="x", pady=5)
        self.dirtext.pack()
        self.changebtn.pack()
        self.progresstotaltext.pack()
        self.progresstotal.pack(fill="both", expand=True)
        self.progresstext.pack()
        self.progress.pack(fill="both", expand=True)

        # chart
        self.chart.pack(fill='both', expand=True, anchor='center')

        # chart buttons
        chartbuttonsframe.pack(side="bottom")
        self.previewcloud.grid(row=0, column=0)
        chartbuttonspacer.grid(row=0, column=1)
        self.chartswitch.grid(row=0, column=2)
        

    # Event handler for "New" in the dropdown menu
        # Method should first check to make sure nothing is running.
        # Then it should do basically the same thing as the new_project method
        # in StartGUI.
    def new_proj_handler(self):
        """
        description
        """
        projdir = fd.askdirectory(title='select workspace', initialdir='/home/')
        if not projdir:
            return
        if ' ' in projdir:
            print("Path must not contain white spaces")
            mb.showerror("Paths cannot contain whitespace                           ")
            return
        self.controller.new_project(projdir)

    # Event handler for "Add Photos" button
        # Method should open a dialogue prompting the user to select img dir
        # Pass directory to controllers add_photos handler
    def photos_handler(self):
        """
        description
        """
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
        """
        Description.
        """
        dialog = BoundsDialog(self)
        if dialog.result: 
            try:
                minx= dialog.result[0]
                maxx= dialog.result[1]
                miny= dialog.result[2]
                maxy= dialog.result[3]
                self.controller.set_bounds(minx, maxx, miny, maxy)
            except Exception as e:
                self.log(e)
                self.log("All fields must contain numbers")

    # Method to be called externally for updating text related to user input
    def update_text(self, numimg):
        """
        description

        Args:
            numimg (type?): what is it?
        """
        self.numimages.config(text=f"Num images: {numimg}")
        

    # Method to be called externally for setting chart image in GUI
    #   Sets the currentchart variable
    #   Requests a Refreshchart event
    def set_chart(self, chartdir):
        """
        description

        Args:
            chartdir (type?): what is it?
        """
        self.currentchart = chartdir
        self.event_generate("<<RefreshChart>>")

    # Method to be called externally for setting example image
    def set_example_image(self, imagefile):
        """
        description

        Args:
            imagefile (type?): what is it?
        """
        img = Image.open(imagefile)
        img = img.resize((150, 100), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        self.exampleimage.config(image=img)
        self.exampleimage.image = img

    # Gives the user an option to chnage the main project directory
    #   If no savefile this will refresh and create a new project
    #   If chosen dir has a savefile this will load the existing project
    def change_projdir(self):
        """
        description
        """
        projdir = fd.askdirectory(title='select workspace', initialdir='/home/')
        if not projdir:
            return
        if ' ' in projdir:
            print("Path must not contain white spaces")
            mb.showerror("Paths cannot contain whitespace                           ")
            return
        self.controller.cancel_recon()   
        for files in self.controller.recentlist:
            if self.controller.picklepath in files[0]:
                self.controller.recentlist.remove(files)
                print("om nom nom nom nom nom")
        self.controller.new_project(projdir, self.controller.projectname, self.controller.imgdir)

    # Event handler for the show files button
    #   Should openthe out dir in file explorer
    def show_files(self):
        """
        description
        """
        show_in_file_manager(str(self.controller.projdir) + "/out")

    # Event handler to be called whenever the window is resized
    #   Updates and scales the chart image with window
    def _resizer(self, e):
        """
        description

        Args:
            e (event): an event?
        """
        image = Image.open(self.currentchart)
        resized_image = self._scale_image(e.width, e.height, image.width, image.height, image)
        self.temp = ImageTk.PhotoImage(resized_image)
        self.chart.itemconfigure(self.chart_image_id, image=self.temp)
    
    # Method writes strings to the log
    def log(self, msg):
        """
        description

        Args:
            msg (type?): what is it?
        """
        self.logtext.insert(END, msg + "\n")
        self.logtext.see("end")

    # Handles chart refresh event
    #    Sets the canvas image to the currentchart
    #    If app has been resized, resizes image to fit
    def _refresh_chart(self, e):
        """
        description

        Args:
            e (event): do we need event? doesn't seem to be used?
        """
        if self.chart.winfo_width() > 1 and self.chart.winfo_height() > 1:
            image = Image.open(self.currentchart)
            resized_image = self._scale_image(self.chart.winfo_width(), self.chart.winfo_height(), image.width, image.height, image)
            self.temp = ImageTk.PhotoImage(resized_image)
        else:
            self.temp = ImageTk.PhotoImage(Image.open(self.currentchart))
        self.chart.itemconfigure(self.chart_image_id, image=self.temp)

    # Scales an image so that it will fit in a window defined by wwidth and wheight
    #   Image scaled without distortion (preserves aspect ratio)
    def _scale_image(self, wwidth, wheight, iwidth, iheight, image):
        """
        description

        Args:
            wwidth (int): window width
            wheight (int): window height
            iwidth (int): ?????
            iheight (int): ?????
            image (image): ?????
        """
        width_scale = wwidth / iwidth
        height_scale = wheight / iheight
        scale = min(width_scale, height_scale)
        new_width = int(iwidth * scale)
        new_height = int(iheight * scale)
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)