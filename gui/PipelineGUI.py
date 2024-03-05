from tkinter import Canvas, Text, END
from tkinter.ttk import Frame, Label, Button, Scrollbar, Progressbar
from ttkbootstrap import Separator
from tkinter import filedialog as fd, messagebox as mb
from PIL import ImageTk, Image
from pathlib import Path
from gui.AppWindow import AppWindow
from gui.BoundsDialog import BoundsDialog
from showinfm import show_in_file_manager
import scripts.RecentsManager as RecentsManager

# TODO: header comments
class PipelineGUI(AppWindow):
    
    # GUI constants
    DEFAULT_CHART = Path(f"gui/placeholder/blankchart.jpg").resolve()
    DEFAULT_PREVIEW = Path(f"gui/placeholder/drone.jpg").resolve()

    def __init__(self, parent, controller, projdir):
        """
        `PipelineGUI` is a class that inherits from :ref:`AppWindow <appwindow>`. It creates and
        manages the internal pages of the app that appear when a project is running. The class
        handles the layout of the GUI and has event handlers for all buttons on the display.

        Args:
            parent (tkinter container): passed from :ref:`main <main>` to make the tkinter frame.
            controller (:ref:`main <main>`\*): a reference to main.
            projdir (pathlib.Path): Project directory containing .pkl file.
        """
        AppWindow.__init__(self, parent, controller)
        self.setup_layout()
        self.projdir = projdir
        self.controller = controller
        self.currentchart = self.DEFAULT_CHART
        self.viewtype = True
        self.bind("<<RefreshChart>>", self._refresh_chart)

    # Setup method for GUI layout and elements
    def setup_layout(self):
        """
        Method that sets up the layout of the GUI, making all elements and placing them. The GUI is
        divided into left and right `tkinter.ttk.Frame` objects, into which chart and pipeline 
        elements are assigned respectively. The elements are packed to ensure order and allow for
        resizing.
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
        self.logtext = Text(right, width=50)
        scrollbar = Scrollbar(right)
        self.logtext['yscrollcommand'] = scrollbar.set
        scrollbar['command'] = self.logtext.yview
        self.cancel = Button(right, text="Cancel", style="cancel.TButton", command=lambda: self.controller.cancel_recon())
        

        ### Left: charts and progress
        self.temp = ImageTk.PhotoImage(Image.open(self.DEFAULT_CHART))
        self.chart = Canvas(self.left)
        self.chart_image_id = self.chart.create_image(0, 0, image=self.temp, anchor='nw')
        self.chart.bind('<Configure>', self._refresh_chart)
        self.previewcloud = Button(chartbuttonsframe, width=20, text="Preview Point Cloud", command=lambda: self.controller.preview_cloud())  # TODO: need to add the handler/command to open the preview.
        self.chartview = Button(chartbuttonsframe, width=20, text="Change View", command=lambda: self.change_chart_view())  # TODO: need to add the handler/command to switch chart

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
        self.chartview.grid(row=0, column=2)

    # Event handler for "Add Photos" button
        # Method should open a dialogue prompting the user to select img dir
        # Pass directory to controllers add_photos handler
    def photos_handler(self):
        """
        Event handler for the "Add Photos" button, the first step in the pipeline. It opens a
        dialog box propting the user to select the directory where their images are saved, which 
        gets passed to the `add_photos()` handler in :ref:`main <main>`.
        It updates the bar internally since it's a nearly instantaneous step.

        .. note::
            Because of how :ref:`Colmap <colmap>` uses file paths, paths (and therefor folders and
            files) cannot contain spaces. This method displays an error message when the user tries
            to use an image directory path that has a space in it.
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
        self.controller.style.configure('prog.Horizontal.TProgressbar', text='100%')

    # Event handler for "Set Bounds" button
        # Method should open a dialogue prompting the user to enter bounds
        # Pass bounds A and B to controllers set_bounds handler
    def bounds_handler(self):
        """
        Event handler for the "Trim Bounds" button, the optional step between the 
        :ref:`Matcher <matcher>` and :ref:`Mesher <mesher>`. It makes a
        :ref:`BoundsDialog <boundsdialog>` object to prompt the user to set the minimum and maximum
        bounds for the x, y, and z axes of the generated point cloud. The inputted values are then
        passed to the `set_bounds` handler in :ref:`main <main>`.
        """
        dialog = BoundsDialog(self)
        if dialog.result: 
            try:
                minx= dialog.result[0]
                maxx= dialog.result[1]
                miny= dialog.result[2]
                maxy= dialog.result[3]
                minz= dialog.result[4]
                maxz= dialog.result[5]
                self.controller.set_bounds(minx, maxx, miny, maxy, minz, maxz)
            except Exception as e:
                self.log(str(e))
                self.log("All fields must contain numbers")

    # Event handler for the show files button
    #   Should open the out dir in file explorer
    def show_files(self):
        """
        Event handler for the "Show Files" button, the last step in the pipeline that opens a
        file explorer window to show the user the contents of the `"out"` folder in the current
        project directory.
        """
        show_in_file_manager(str(self.controller.projdir) + "/out")

    # Method to be called externally for updating text related to user input
    def update_text(self, numimg):
        """
        Method used to update the text displaying the number of images in the current image
        directory on the right button bar. Used by :ref:`main <main>` when making a new project,
        opening an existing project, and when adding images/selecting an image directory. 

        Args:
            numimg (int): the number of images in the current image directory.
        """
        self.numimages.config(text=f"Num images: {numimg}")
        

    # Method to be called externally for setting chart image in GUI
    #   Sets the currentchart variable
    #   Requests a Refreshchart event
    def set_chart(self, chartdir):
        """
        Method to be called externally to set the chart image in the GUI. It's called in 
        :ref:`main <main>` when the state is updated or bounds are set.
        Because of how different threads interact with the TK app, the chart
        uses a `RefreshChart` event to actually change, which the handler requests.

        Args:
            chartdir (pathlib.Path): the path to the current chart to display.
        """
        self.currentchart = chartdir
        self.event_generate("<<RefreshChart>>")

    def change_chart_view(self):
        """
        Event handler for the "Change View" button under the chart, toggles between the heat map 
        and elevation map views. Because of how different threads interact with the TK app, the 
        chart uses a `RefreshChart` event to actually change, which the handler generates.
        """
        self.viewtype = ~self.viewtype # Toggle boolean
        # TODO: set current chart (self.currentchart) and then refresh chart event will handle the rest
        self.event_generate("<<RefreshChart>>")

    # Method to be called externally for setting example image
    def set_example_image(self, imagefile):
        """
        Method called externally to set the example image on the top right of the app. It allows
        the user to confirm that they've selected the right image directory before progressing
        through the pipeline.

        Args:
            imagefile (pathlib.Path): the path to the example image to display.
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
        Event handler for the "Change" button under the printed workspace path, which gives the 
        user an option to change the project directory. It makes a new project with the same name
        and image directory and removed the original from recents projects.
        If the user doesn't select a new project directory (or if the path has a
        space), then the project directory doesn't change.
        """
        projdir = fd.askdirectory(title='select workspace', initialdir='/home/')
        if not projdir:
            return
        if ' ' in projdir:
            print("Path must not contain white spaces")
            mb.showerror("Paths cannot contain whitespace                           ")
            return
        self.controller.cancel_recon()   
        # don't want it to be in recents if we're moving away from the old file path.
        RecentsManager.remove(self.controller.picklepath)
        self.controller.new_project(projdir, self.controller.projectname, self.controller.imgdir)
    
    # Method writes strings to the log
    def log(self, msg):
        """
        Method that writes strings to the log for display in the log textbox. Sets the log display
        to show the bottom of the log.

        Args:
            msg (string): what is it?
        """
        self.logtext.insert(END, msg + "\n")
        self.logtext.see("end")

    # Handles chart refresh event
    #    Sets the canvas image to the currentchart
    #    If app has been resized, resizes image to fit
    def _refresh_chart(self, e):
        """
        Event handler called whenever a `RefreshChart` events occurs (in set_chart() and
        change_chart_view()). It sets the image displayed on the `chart` canvas to the currentchart
        set by `set_chart()`. If the Tk app has been resized, then the chart image is resized,
        using `_scale_image()`, to fit in the left column.

        Args:
            e (event): a `RefreshChart` or `Configure` event

        .. note::
            May need to change the description for this function depending on if we change _resizer
            or not.
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
        Helper method that scales an image to fit within a window defined by its width (wwidth)
        and height (wheight). It scales images without distortion (preserving the aspect ratio)
        by choosing the smaller scale calculated from the x and y axes.

        Args:
            wwidth (int): window width
            wheight (int): window height
            iwidth (int): image width
            iheight (int): image height
            image (image): the image `(chart)` to be scaled
        """
        width_scale = wwidth / iwidth
        height_scale = wheight / iheight
        scale = min(width_scale, height_scale)
        new_width = int(iwidth * scale)
        new_height = int(iheight * scale)
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)  