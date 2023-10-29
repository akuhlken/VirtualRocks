
import tkinter as tk

root = tk.Tk()
root.geometry("1000x1000")
root.title("VirtualRocks")

label = tk.Label(root, text="Hello World", font=('Arial', 18))
label.pack(padx=20, pady=20)

#textbox = tk.Text(root, font=('Arial', 16))
#textbox.pack()

myentry = tk.Entry(root)
myentry.pack()

button1 = tk.Button(root, text='Click Me', font=('Arial', 16))
button1.pack()

root.mainloop()     