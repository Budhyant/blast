import tkinter as tk
from PIL import ImageTk, Image

path = './dimension.png'

root = tk.Tk()
img = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(root, image = img)
# panel.pack(side = "bottom", fill = "both", expand = "yes")
panel.pack()
root.mainloop()
