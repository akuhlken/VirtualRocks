import tkinter as tk

def change_button_text():
    new_text = "New Text"  # Replace with the text you want to set
    button.config(text=new_text)

app = tk.Tk()
app.title("Change Button Text Example")

button = tk.Button(app, text="Original Text", command=change_button_text)
button.pack()

app.mainloop()