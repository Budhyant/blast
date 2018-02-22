from eval_param import Evaluate
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk
LARGE_FONT = ("Verdana", 12)

param_result = Evaluate(25, 25, 1)
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

        # tk.Tk.iconbitmap(self, default="")
        tk.Tk.wm_title(self, "AIRBLAST PARAMETERS")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame = Landing(container, self)
        self.frames['Render'] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class Landing(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="AIRBLAST PARAMETERS BY NEQ & TNT EQUIVALENCE", font=LARGE_FONT)
        label.grid(row=0, column=0, columnspan=1, padx=5, pady=5)

        label_1 = tk.Label(self, text="Actual Stand-off Distance (D)[m]")
        label_2 = tk.Label(self, text="Net Explosive Quantity (Q)[kg]")
        label_3 = tk.Label(self, text="select your bomb type")
        label_4 = tk.Label(self, text="select your calc type")

        label_1.grid(row=1, column=0)
        label_2.grid(row=2, column=0)
        label_3.grid(row=3, column=0)
        label_4.grid(row=4, column=0)

        e1 = tk.Entry(self, width=3)
        e2 = tk.Entry(self, width=3)
        e1.grid(row=1, column=1)
        e2.grid(row=2, column=1)
        e1.focus_set()
        e2.focus_set()


        bomb_type = tk.StringVar(self)
        bomb_type.set("TNT") # initial value
        cal_type = tk.StringVar(self)
        cal_type.set("air") # initial value

        option_1 = tk.OptionMenu(self, bomb_type, "TNT", "RDX", "HMX", "Nitroglycerin", "CompoundB", "Semtex", "60% Nitroglycerin dynamite")
        option_1.grid(row=3, column=1)
        option_2 = tk.OptionMenu(self, cal_type, "air", "surface")
        option_2.grid(row=4, column=1)

        so_dist = None
        ne_qty = None
        TNT_EQ_FIG = None
        cal_type = None

        def set_TNT_EQ_FIG(val):
            if val == 'TNT':
                return 1
            elif val == 'RDX':
                return 1.185
            elif val == 'HMX':
                return 1.256
            elif val == 'Nitroglycerin':
                return 1.481
            elif val == 'CompoundB':
                return 1.148
            elif val == 'Semtex':
                return 1.25
            elif val == '60% Nitroglycerin dynamite':
                return 0.6

            return

        def callback():
            print('type e1', type(int(e1.get())), e1.get())
            if type(e1.get()) == int and type(e2.get()) == int:
                so_dist = e1.get()
                ne_qty = e2.get()
                TNT_EQ_FIG = set_TNT_EQ_FIG(bomb_type.get())
                cal_type = cal_type.get()
                print('bomb type', bomb_type)
                print('cal_type', cal_type)
                # compute param using Evaluate Class

            else:
                label_err = tk.Label(self, text="please type integer input only")
                label_err.grid(row=3, column=1)
            return

        btn_calc = tk.Button(self, text="calculate", width=10, command=callback)
        btn_calc.grid(row=5, column=0)


# class Air(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Air", font=LARGE_FONT)
#         label.pack(pady=10, padx=10)

#         button1 = ttk.Button(self, text="Back to Home",
#                             command=lambda: controller.show_frame(Landing))
#         button1.pack()

#         f1 = Figure(figsize=(5,5), dpi=100)
#         a = f1.add_subplot(111)
#         a.plot(pt_air_fr_pr['x'], pt_air_fr_pr['y'])
#         a.plot(pt_air_fr_ps['x'], pt_air_fr_ps['y'])
#         a.plot([pt_air_fr_pr['x'][1], pt_air_fr_pr['x'][1]], [0, pt_air_fr_pr['y'][1]], '--')
#         # a.xlabel('time (t)')
#         # a.ylabel('pressure (kpa)')

#         f2 = Figure(figsize=(5,5), dpi=100)
#         b = f2.add_subplot(111)
#         b.plot(pt_air_eq['x'], pt_air_eq['y'])
#         # b.xlabel('time (t)')
#         # b.ylabel('pressure (kpa)')

#         # plt.show()
#         canvas1 = FigureCanvasTkAgg(f1, self)
#         canvas1.show()

#         # toolbar = NavigationToolbar2TkAgg(canvas1, self)
#         # toolbar.update()
#         canvas1._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
#         # canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

#         canvas2 = FigureCanvasTkAgg(f2, self)
#         canvas2.show()

#         # toolbar = NavigationToolbar2TkAgg(canvas2, self)
#         # toolbar.update()
#         canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
#         # canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# class Surface(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Surface", font=LARGE_FONT)
#         label.pack(pady=10, padx=10)

#         button1 = ttk.Button(self, text="Back to Home",
#                             command=lambda: controller.show_frame(Landing))
#         button1.pack()

#         f1 = Figure(figsize=(5,5), dpi=100)
#         a = f1.add_subplot(111)
#         a.plot(pt_sfc_fr_pr['x'], pt_sfc_fr_pr['y'])
#         a.plot(pt_sfc_fr_ps['x'], pt_sfc_fr_ps['y'])
#         a.plot([pt_sfc_fr_pr['x'][1], pt_sfc_fr_pr['x'][1]], [0, pt_sfc_fr_pr['y'][1]], '--')
#         # a.xlabel('time (t)')
#         # a.ylabel('pressure (kpa)')

#         f2 = Figure(figsize=(5,5), dpi=100)
#         b = f2.add_subplot(111)
#         b.plot(pt_sfc_eq['x'], pt_sfc_eq['y'])
#         # b.xlabel('time (t)')
#         # b.ylabel('pressure (kpa)')

#         # plt.show()
#         canvas1 = FigureCanvasTkAgg(f1, self)
#         canvas1.show()

#         # toolbar = NavigationToolbar2TkAgg(canvas1, self)
#         # toolbar.update()
#         canvas1._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
#         # canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

#         canvas2 = FigureCanvasTkAgg(f2, self)
#         canvas2.show()

#         # toolbar = NavigationToolbar2TkAgg(canvas2, self)
#         # toolbar.update()
#         canvas2._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
#         # canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

app = Blast()
app.mainloop()
