
import tkinter as tk

root = tk.Tk()
root.geometry("800x500")
root.title("VirtualRocks")

label = tk.Label(root, text="Hello World", font=('Arial', 18))
label.pack(padx=20, pady=20)

textbox = tk.Text(root, font=('Arial', 16))
textbox.pack()

root.mainloop()