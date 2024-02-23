from tkinter import Button
from tkinter.ttk import Label, Frame
from gui.AppWindow import AppWindow

class StartGUI(AppWindow):

    def __init__(self, parent, controller, recents):
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
        