from tkinter import Button
from tkinter.ttk import Label, Frame
from gui.AppWindow import AppWindow

# TODO: Class description
class StartGUI(AppWindow):

    def __init__(self, parent, controller):
        """
        `StartGUI` is a subclass of :ref:`AppWindow <appwindow>` and creates the front page of the
        Tk app. It has the menu bar from :ref:`AppWindow <appwindow>` and has button to allow the
        user to make a new project or open an existing project.

        Args:
            parent (tkinter container): passed from :ref:`main <main>` to make the tkinter frame.
            controller (:ref:`main <main>`\*): a reference to main.
        """
        AppWindow.__init__(self, parent, controller)

        # making the elements of the start menu
        title = Label(self, text="Choose Project:", anchor="center", style="title.TLabel")
        middleframe = Frame(self)
        newBtn = Button(middleframe, height=10, width=20, text="New", relief="groove", command=lambda: self.new_project())
        openBtn = Button(middleframe, height=10, width=20, text="Open", relief="groove", command=lambda: self.open_project())
        label = Label(self, text="*paths cannot contain white spaces")

        # packing the menu elements in the right order
        title.pack(side="top", fill="x", pady=10)
        middleframe.place(anchor="c", relx=.5, rely=.5)
        newBtn.pack(padx=20, side='left')
        openBtn.pack(padx=20, side='right')
        label.pack(side='bottom')
        