from eval_param import GetParamsForPlot
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk
LARGE_FONT = ("Verdana", 12)

param_result = GetParamsForPlot()
print('result', param_result.get_points())


class Blast(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="")
        tk.Tk.wm_title(self, "BTC title")

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame = Render(container, self)
        self.frames['Render'] = frame
        frame.grid(row=0, column=0, sticky="nsew")


class Render(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="calculate",
                            command=lambda: print('calculate button clicked'))
        button1.pack()

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8], [1,2,3,4,5,6,7,8])
        a.plot([1,2,3,4,5,6,7,8], [8,7,6,5,4,3,2,1])

        # plt.show()
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

app = Blast()
app.mainloop()
