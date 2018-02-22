from eval_param import GetParamsForPlot
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk
LARGE_FONT = ("Verdana", 12)

param_result = GetParamsForPlot()
points = param_result.get_points()
pt_air = points['air']
pt_air_fr = pt_air['front-wall']
pt_air_fr_pr = pt_air_fr['pr']
pt_air_fr_ps = pt_air_fr['ps']
pt_air_eq = pt_air['equivalent']

pt_sfc = points['surface']
pt_sfc_fr = pt_sfc['front-wall']
pt_sfc_fr_pr = pt_sfc_fr['pr']
pt_sfc_fr_ps = pt_sfc_fr['ps']
pt_sfc_eq = pt_sfc['equivalent']

class Blast(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="")
        tk.Tk.wm_title(self, "AIRBLAST PARAMETERS")

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # frame = Render(container, self)
        # self.frames['Render'] = frame
        # frame.grid(row=0, column=0, sticky="nsew")

        for F in (Air, Surface, Landing):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=1, sticky="nsew")
            self.show_frame(F)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class Landing(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="AIRBLAST PARAMETERS\nBY NEQ & TNT EQUIVALENCE", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Air",
                            command=lambda: controller.show_frame(Air))
        button1.pack()

        button3 = ttk.Button(self, text="Surface",
                            command=lambda: controller.show_frame(Surface))
        button3.pack()

class Air(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Air", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(Landing))
        button1.pack()

        f1 = Figure(figsize=(5,5), dpi=100)
        a = f1.add_subplot(111)
        a.plot(pt_air_fr_pr['x'], pt_air_fr_pr['y'])
        a.plot(pt_air_fr_ps['x'], pt_air_fr_ps['y'])
        a.plot([pt_air_fr_pr['x'][1], pt_air_fr_pr['x'][1]], [0, pt_air_fr_pr['y'][1]], '--')
        # a.xlabel('time (t)')
        # a.ylabel('pressure (kpa)')

        f2 = Figure(figsize=(5,5), dpi=100)
        b = f2.add_subplot(111)
        b.plot(pt_air_eq['x'], pt_air_eq['y'])
        # b.xlabel('time (t)')
        # b.ylabel('pressure (kpa)')

        # plt.show()
        canvas1 = FigureCanvasTkAgg(f1, self)
        canvas1.show()

        # toolbar = NavigationToolbar2TkAgg(canvas1, self)
        # toolbar.update()
        canvas1._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        canvas2 = FigureCanvasTkAgg(f2, self)
        canvas2.show()

        # toolbar = NavigationToolbar2TkAgg(canvas2, self)
        # toolbar.update()
        canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class Surface(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Surface", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(Landing))
        button1.pack()

        f1 = Figure(figsize=(5,5), dpi=100)
        a = f1.add_subplot(111)
        a.plot(pt_sfc_fr_pr['x'], pt_sfc_fr_pr['y'])
        a.plot(pt_sfc_fr_ps['x'], pt_sfc_fr_ps['y'])
        a.plot([pt_sfc_fr_pr['x'][1], pt_sfc_fr_pr['x'][1]], [0, pt_sfc_fr_pr['y'][1]], '--')
        # a.xlabel('time (t)')
        # a.ylabel('pressure (kpa)')

        f2 = Figure(figsize=(5,5), dpi=100)
        b = f2.add_subplot(111)
        b.plot(pt_sfc_eq['x'], pt_sfc_eq['y'])
        # b.xlabel('time (t)')
        # b.ylabel('pressure (kpa)')

        # plt.show()
        canvas1 = FigureCanvasTkAgg(f1, self)
        canvas1.show()

        # toolbar = NavigationToolbar2TkAgg(canvas1, self)
        # toolbar.update()
        canvas1._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        canvas2 = FigureCanvasTkAgg(f2, self)
        canvas2.show()

        # toolbar = NavigationToolbar2TkAgg(canvas2, self)
        # toolbar.update()
        canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

app = Blast()
app.mainloop()
