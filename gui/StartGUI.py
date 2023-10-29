import tkinter as tk

class StartGUI(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Project:", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        middleframe = tk.Frame(self)
        middleframe.place(anchor="c", relx=.5, rely=.5)

        newBtn = tk.Button(middleframe, text="New", command=lambda: controller.start_project('/temp/path/to/project'))
        openBtn = tk.Button(middleframe, text="Open", command=lambda: controller.start_project('/temp/path/to/project'))

        newBtn.pack(padx=20, side='left')
        openBtn.pack(padx=20, side='right')