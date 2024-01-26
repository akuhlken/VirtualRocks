import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

class HelpMenuGUI(tttk.Window):

    def __init__(self, parent, controller):
        
        # General layout idea:
        #   like a classic documentation website
        #   sidebar menu with nested dropdowns. outermost layer (highest level) is darker
        #   color while everything else is lighter (could flip for dark mode). Selected
        #   item is highlighted in the menu.
        #   Right side of the window is dedicated to the content relevant to whatever menu
        #   item was selected. Should be scrollable. 
        #   Resize should make the bar longer to fill the new window size but not wider.

        self.popoutmenu = tk.Toplevel(takefocus=True)
        self.popoutmenu.title("Help Menu")

        
        self.controller = controller

        sidemenu = ttk.Frame(self.popoutmenu, bootstyle="dark", width="200")
        sidemenu.pack(side="left", fill="y")

        menutext = tttk.ScrolledText(self.popoutmenu, width ="600") # hbar=False, autohide=True
        menutext.pack(side="right", fill="both")

        self.popoutmenu.geometry("800x550")
        '''


        middleframe = ttk.Frame(self)
        middleframe.place(anchor="c", relx=.5, rely=.5)

        newBtn = tk.Button(middleframe, height=10, width=20, text="New", bg=controller.buttoncolor, relief="groove", command=lambda: self.new_project())
        openBtn = tk.Button(middleframe, height=10, width=20, text="Open", bg=controller.buttoncolor, relief="groove", command=lambda: self.open_project())
        label = ttk.Label(self, text="*paths cannot contain white spaces")

        newBtn.pack(padx=20, side='left')
        openBtn.pack(padx=20, side='right')
        label.pack(side='bottom')
        '''
