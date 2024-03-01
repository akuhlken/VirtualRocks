import tkinter as tk
from tkinter import simpledialog

# TODO: Header comments
class BoundsDialog(simpledialog.Dialog):
    def body(self, master):
        """
        description

        Args:
            master (type?): what is it?
        """
        self.title("Remove Points:")
        self.labels = ["min X:", "max X:", "min Y:", "max Y:", "min Z:", "max Z:"]
        self.entries = []
        for i in range(6):
            tk.Label(master, text=self.labels[i]).grid(row=i, column=0)
            entry = tk.Entry(master)
            entry.grid(row=i, column=1)
            self.entries.append(entry)
        return self.entries[0]  # initial focus

    def apply(self):
        """
        description
        """
        try:
            self.result = []
            for i, entry in enumerate(self.entries):
                if not entry.get():
                    if i % 2 == 0:
                        self.result.append(float('-inf'))
                    else:
                        self.result.append(float('inf'))
                else:
                    self.result.append(float(entry.get()))
        except Exception as e:
            print(e)

# import tkinter as tk
# from tkinter import simpledialog, messagebox

# class CustomDialog(simpledialog.Dialog):
#     def body(self, master):
#         self.entry_fields = []
#         for i in range(6):
#             entry = tk.Entry(master)
#             entry.insert(0, "10000")
#             entry.pack()
#             self.entry_fields.append(entry)
#         return self.entry_fields[0]  # initial focus

#     def validate(self):
#         entries = [entry.get() for entry in self.entry_fields]
#         if self.validate_floats(*entries):
#             return True
#         else:
#             messagebox.showerror("Error", "Invalid input. Please enter floating point numbers only.")
#             return False

#     def apply(self):
#         entries = [entry.get() for entry in self.entry_fields]
#         messagebox.showinfo("Success", f"All inputs are valid: {entries}")

#     @staticmethod
#     def validate_floats(*args):
#         for arg in args:
#             try:
#                 float(arg) if arg else 10000.0
#             except ValueError:
#                 return False
#         return True

# root = tk.Tk()
# root.withdraw()  # hide main window
# dialog = CustomDialog(root)
# root.mainloop()