from tkinter import Button
from tkinter.ttk import Label, Frame
from gui.AppWindow import AppWindow

# TODO: Class description
class StartGUI(AppWindow):

    def __init__(self, parent, controller, recents):
        """
        description of the whole class

        Args:
            parent (tkinter container): passed from :ref:`main <main>` to make the tkinter frame.
            controller (:ref:`main <main>`\*): a reference to main.
            recents (:ref:`recents <recentsmanager>` object): a RecentsManager object that stores and maintains the dictionary of recent projects.
        """
        AppWindow.__init__(self, parent, controller, recents)
        self.controller = controller
        label = Label(self, text="Choose Project:", anchor="center", style="title.TLabel")
        label.pack(side="top", fill="x", pady=10)

        middleframe = Frame(self)
        middleframe.place(anchor="c", relx=.5, rely=.5)

        newBtn = Button(middleframe, height=10, width=20, text="New", bg=controller.buttoncolor, relief="groove", command=lambda: self.new_project())
        openBtn = Button(middleframe, height=10, width=20, text="Open", bg=controller.buttoncolor, relief="groove", command=lambda: self.open_project())
        label = Label(self, text="*paths cannot contain white spaces")

        newBtn.pack(padx=20, side='left')
        openBtn.pack(padx=20, side='right')
        label.pack(side='bottom')
        