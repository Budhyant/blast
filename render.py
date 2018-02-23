from eval_param import Evaluate
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk
LARGE_FONT = ("Verdana", 12)

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
        label = tk.Label(self, text="AIRBLAST PARAMETERS\nBY NEQ & BY TNT EQUIVALENCE", font=LARGE_FONT, fg="blue")
        label.config(font=('Courier', 25))
        label.grid(row=0, column=0, columnspan=1, padx=10, pady=30)

        label_1 = tk.Label(self, text="Actual Stand-off Distance (D)[m]")
        label_2 = tk.Label(self, text="Net Explosive Quantity (Q)[kg]")
        label_3 = tk.Label(self, text="select your bomb type")
        label_4 = tk.Label(self, text="select your calc type")

        label_1.grid(row=1, column=0, pady=15, sticky="E")
        label_2.grid(row=2, column=0, pady=15, sticky="E")
        label_3.grid(row=3, column=0, pady=15, sticky="E")
        label_4.grid(row=4, column=0, pady=15, sticky="E")

        e1 = ttk.Entry(self, width=3)
        e2 = ttk.Entry(self, width=3)
        e1.grid(row=1, column=1, padx=10, pady=15)
        e2.grid(row=2, column=1, padx=10, pady=15)
        e1.focus_set()
        e2.focus_set()


        bomb_type = tk.StringVar(self)
        bomb_type.set("TNT") # initial value
        cal_type = tk.StringVar(self)
        cal_type.set("air") # initial value
        print('cal_type.get()', cal_type.get())
        option_1 = ttk.OptionMenu(self, bomb_type, "TNT", "RDX", "HMX", "Nitroglycerin", "CompoundB", "Semtex", "60% Nitroglycerin dynamite")
        option_1.grid(row=3, column=1, padx=10, pady=11)
        option_2 = ttk.OptionMenu(self, cal_type, "air", "surface")
        option_2.grid(row=4, column=1, padx=10, pady=11)

        so_dist = None
        ne_qty = None

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
            if e1.get() == '' or e2.get() == '':
                label_err = tk.Label(self, text="please type input values", fg="red")
                label_err.grid(row=5, column=1)
            # elif type(int(e1.get())) == int and type(int(e2.get())) == int:
            elif self.validateFloat(e1.get()) and self.validateFloat(e2.get()):
                label_ok = tk.Label(self, text="   all input values are OK   ", fg="black")
                label_ok.grid(row=5, column=1)
                so_dist = float(e1.get())
                ne_qty = float(e2.get())
                TNT_EQ_FIG = set_TNT_EQ_FIG(bomb_type.get())
                cal_type_val = cal_type.get()
                print('bomb type', bomb_type.get())
                print('cal_type', cal_type_val)
                # compute param using Evaluate Class
                if cal_type_val == 'air':
                    self.plot_air(so_dist, ne_qty, TNT_EQ_FIG)
                else:
                    self.plot_sfc(so_dist, ne_qty, TNT_EQ_FIG)

            else:
                label_err = tk.Label(self, text="please type integer input only", fg="red")
                label_err.grid(row=5, column=1)
                print('e1.get type', type(e1.get()), 'e2.get type', type(e2.get()))
            return
        ttk.Style().configure('white/gray.TButton', foreground='black', background='gray')
        btn_calc = ttk.Button(self, text="calculate", style='white/gray.TButton', command=callback)
        btn_calc.grid(row=5, column=0, padx=10, pady=20, sticky="E")

    def validateFloat(self, value):
        ENTRY = value.strip()
        if ENTRY == "": return # do noting if we don't have a value
        try:
            NUMENTRY = float(ENTRY)
            if NUMENTRY: return True
        except ValueError:
            print('the input value is not integer or float')
            return

    def plot_air(self, so_dist, ne_qty, TNT_EQ_FIG):
        param_result = Evaluate(so_dist, ne_qty, TNT_EQ_FIG)
        points = param_result.get_points()
        pt_air = points['air']
        pt_air_fr = pt_air['front-wall']
        pt_air_fr_pr = pt_air_fr['pr']
        pt_air_fr_ps = pt_air_fr['ps']
        pt_air_eq = pt_air['equivalent']

        f1 = Figure(figsize=(4,4), dpi=100)
        a = f1.add_subplot(111)
        a.set_title('Front-Wall Loading')
        a.plot(pt_air_fr_pr['x'], pt_air_fr_pr['y'])
        a.annotate('Pr', xy=(0.9, 0.9))
        a.plot(pt_air_fr_ps['x'], pt_air_fr_ps['y'])
        a.plot([pt_air_fr_pr['x'][1], pt_air_fr_pr['x'][1]], [0, pt_air_fr_pr['y'][1]], '--')
        canvas1 = FigureCanvasTkAgg(f1, self)

        f2 = Figure(figsize=(4,4), dpi=100)
        b = f2.add_subplot(111)
        b.set_title('Equivalent Loading')
        b.plot(pt_air_eq['x'], pt_air_eq['y'])
        canvas2 = FigureCanvasTkAgg(f2, self)

        canvas1.show()
        canvas2.show()
        canvas1._tkcanvas.grid(row=0, rowspan=6, column=2)
        canvas2._tkcanvas.grid(row=7, column=2)

    def plot_sfc(self, so_dist, ne_qty, TNT_EQ_FIG):
        param_result = Evaluate(so_dist, ne_qty, TNT_EQ_FIG)
        points = param_result.get_points()

        pt_sfc = points['surface']
        pt_sfc_fr = pt_sfc['front-wall']
        pt_sfc_fr_pr = pt_sfc_fr['pr']
        pt_sfc_fr_ps = pt_sfc_fr['ps']
        pt_sfc_eq = pt_sfc['equivalent']

        f1 = Figure(figsize=(4,4), dpi=100)
        a = f1.add_subplot(111)
        a.plot(pt_sfc_fr_pr['x'], pt_sfc_fr_pr['y'])
        a.plot(pt_sfc_fr_ps['x'], pt_sfc_fr_ps['y'])
        a.plot([pt_sfc_fr_pr['x'][1], pt_sfc_fr_pr['x'][1]], [0, pt_sfc_fr_pr['y'][1]], '--')
        canvas1 = FigureCanvasTkAgg(f1, self)

        f2 = Figure(figsize=(4,4), dpi=100)
        b = f2.add_subplot(111)
        b.plot(pt_sfc_eq['x'], pt_sfc_eq['y'])
        canvas2 = FigureCanvasTkAgg(f2, self)

        canvas1.show()
        canvas2.show()
        canvas1._tkcanvas.grid(row=0, rowspan=6, column=2)
        canvas2._tkcanvas.grid(row=7, column=2)


app = Blast()
app.mainloop()
