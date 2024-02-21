import tkinter as tk
from tkinter import simpledialog

class BoundsDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("Remove Points:")
        self.labels = ["min X:", "max X:", "min Y:", "max Y:"]
        self.entries = []
        for i in range(4):
            tk.Label(master, text=self.labels[i]).grid(row=i, column=0)
            entry = tk.Entry(master)
            entry.grid(row=i, column=1)
            self.entries.append(entry)
        return self.entries[0]  # initial focus

    def apply(self):
        self.result = []
        for entry in self.entries:
            self.result.append(float(entry.get()))