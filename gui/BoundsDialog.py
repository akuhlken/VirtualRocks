from tkinter import simpledialog, Label, Entry

# TODO: Header comments
class BoundsDialog(simpledialog.Dialog):
    """
    `BoundsDialog` initializes a dialog that prompts the user to input bounds for the current
    point cloud. 
    """
    def body(self, master):
        """
        Method that creates the physical dialog box, allowing users to enter the bounds for the x,
        y, and z axes.

        Args:
            master (:ref:`PipelineGUI <pipelineGUI>`\* instance): the current instance of `PipelineGUI` class.
        """
        self.title("Remove Points:")
        self.labels = ["min X:", "max X:", "min Y:", "max Y:", "min Z:", "max Z:"]
        self.entries = []
        for i in range(6):
            Label(master, text=self.labels[i]).grid(row=i, column=0)
            entry = Entry(master)
            entry.grid(row=i, column=1)
            self.entries.append(entry)
        return self.entries[0]  # initial focus

    def apply(self):
        """
        Method to loop through the inputted values and make the values usable by the app. 

        For boxes that did not get values inputted, their values are set to defaults to avoid
        undesired crops (min prompts = negative infinity, max prompts = positive infinity).
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
